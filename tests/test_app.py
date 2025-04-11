import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Super secure' in response.data

def test_xss_route(client):
    response = client.get('/xss?input=pytest', follow_redirects=True)
    assert response.status_code == 200
    assert b'pytest' in response.data

def test_user_route_get(client):
    response = client.get('/user', follow_redirects=True)
    assert response.status_code == 200
    assert b'Username:' in response.data