from flask import Flask, request, render_template_string
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
import hashlib, os

app = Flask(__name__)
Talisman(app, content_security_policy=None) #mitigating security headers

#mitigated secret key vulnerability (render.com env variable)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

#unsafe database setup example
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

with app.app_context():
    db.create_all()

#weak password hashing
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/')
def index():
    return 'Super secure Flask application'

#cross site scripting vulerability endpoint
@app.route('/xss')
def xss():
    user_input = request.args.get('input', '')
    safe_input = escape(user_input) #mitigated xss vulnerability
    return render_template_string("<h1>Input was = {{user_input}}</h1>",input=safe_input)

#sql injection vulerability
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        #no input validation
        query = f"INSERT INTO user (username, password_hash) VALUES ('{username}', '{hashed_password}')"
        db.session.execute(query)
        db.session.commit()
        return 'User created'
    return '''
        <form method="POST">
            Username: <input name="username">
            Password: <input name="password" type="password">
            <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)