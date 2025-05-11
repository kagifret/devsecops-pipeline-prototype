# DevSecOps pipeline prototype

## Overview
The source code and pipeline configuration for my DevSecOps pipeline prototype can be located in this repository. It is part of my Bachelor thesis as a prototype to collect the findings in terms of effectivess in finding security vulnerabilities in early development stages via iterative testing and deployment. It features a simple Flask web application with intentional vulnerabilities. This prototype integrates security tools like SonarCloud, Snyk and OWASP ZAP. Additionally Pytest is used for unit testing. The pipeline is hosted on GitHub Actions as a CI/CD workflow. The web app is deployed to the "Render.com" environtment for accessibility. 

## Structure
- `/`: Flask source code (`app.py`), dependencies (`requirements.txt`), and Docker configuration (`Dockerfile`)
- `/tests`:  Pytest unit tests (`test_app.py`)
- `.github/workflows`: GitHub Actions pipeline configuration and (`pipeline.yaml`) defines the CI/CD stages

## Features
- **Flask Web Application:** Simple Python web app with intentional vulnerabilities for testing purposes
- **Automated CI/CD Pipeline:** Uses GitHub Actions for build, test and security scanning
- **Unit Testing:** Uses Pytest to ensure basic application functionality
- **Static Application Security Testing (SAST):** Used SonarCloud for analyzing code quality and security issues in the source code
- **Software Composition Analysis (SCA):** Used Snyk to detect vulnerabilities in application dependencies and the Docker packages
- **Dynamic Application Security Testing (DAST):** Used OWASP ZAP's baseline scan to detect runtime vulnerabilities
- **Security Headers:** Basic implementation using Flask-Talisman
- **Containerization:** Application was packaged using Docker
- **Cloud Deployment:** Hosted on Render.com's free tier

## Setup and installation instructions

### Prerequisites
Before you begin, make sure you have the following installed:
- **Git:** for cloning the repository
- **Python:** version 3.12 or later
- **pip:** Python package installer
- **Docker:** for building and running the container locally
- **GitHub Account:** for hosting the repository and using GitHub Actions
- **Render.com Account:** A free tier account is sufficient for deployment
- **SonarCloud Account:** is required for SAST scans (free for public repositories)
- **Snyk Account:** is required for SCA scans (free tier available)



### 1. Clone the repository
Clone the repository to your local machine:
```bash
git clone https://github.com/kagifret/devsecops-pipeline-prototype.git
cd devsecops-pipeline-prototype
```

or use VS Code internal functionality of Git cloning with the URL of this repository

- **Python Virtual Environment (for local development)**
To ensure the activation of the virtual environment, create one after cloning the repository by using the following commands:
```bash
#first navigate to the project's directory (after previous step)
python -m venv venv

#run .\venv\Scripts\activate if Windows 
#or source venv/bin/activate on MacOS/Linux 

#run after activating the virtual environment to install require python libraries
pip install -r requirements.txt

#test the flask app
flask run --host=0.0.0.0
```
**In case if the Flask application does not run**
Try this method by manually inserting a "FLASK_VAR" environment variable
```bash
set FLASK_VAR= value #for Windows, replace "value" with your desired value
$env:FLASK_VAR= 'value' #for Windows PowerShell
export FLASK_VAR='value' #for MacOS/Linux

#try running again
flask run --host=0.0.0.0
```
### 1.1 Bulding and running a local Docker instance
Optional step if you need to run a local Docker instance of this project, since the primary goal is to run the web application via CI/CD pipeline and the Docker instance being deployed on Render.com.
Before proceeding, make sure to have a Docker Desktop and Docker Engine applications running on your local machine.

1. Go to your project's root folder (devsecops-pipeline-prototype) directory. Check if it contains a Dockerfile.
2. Build the Docker image:
   ```bash
   docker build -t devsecops-prototype .
   ```

  * "-t name" tags the Docker image with the name "name"
  * "." indicates that the Dockerfile is in the "current" directory
  
3. Running the Docker container
   ```bash
   docker run --rm -p 5000:5000 -e FLASK_VAR='value' devsecops-prototype
   ```

   * "--rm" automatically removes the container after running
   * "-p 5000:5000" maps the port from your machine to to the container's port
   * "-e FLASK_VAR='value' " sets the required environment variable (replace it with any value)
   * "devsecops-ptototype" specifies which image to run to Docker
  
4. Accessing the web application
    Open your browser, navigate to "http://localhost:5000". You should see the Flask web application running successfully.
5. Stopping the container
   Press "Ctrl + C" in the terminal window, in which the "docker run" command was executed. The container should stop running immediately.

### 2. Configuring secrets for GitHub Actions
The pipeline requires API tokens and secrets in order to use SonarCloud and Snyk scanning tools. They need to be configured in your GitHub repository settings:
1. Go to your repository page on GitHub
2. Navigate to `Settings` => `Secrets and variables`  => `Actions`.
3. Locate `Repository secrets` and press `New repository secret` for each of the following:

    *   **Secret Name:** `SONAR_TOKEN`
        *   **Value:** SonarCloud API Token
        *   **How to get:**
            1. Log in to [SonarCloud.io](https://sonarcloud.io/)
            2. Click your profile picture on top right
            3. Go to My Account => Security tab
            4. Under "Generate Tokens", enter a name for it and click `Generate`
            5. Copy the generated token value (it wont be shown again) and paste it as the secret's value in GitHub

    *   **Secret Name:** `SNYK_TOKEN`
        *   **Value:** Snyk API Token.
        *   **How to get:**
            1. Log in to [app.snyk.io](https://app.snyk.io/)
            2. Navigate to Account Settings on the bottom left
            3. Locate the General tab and find Auth Token section
            4. Generate an API key
            5. Copy the API token value and paste it as the secret's value in GitHub

    *   **Secret Name:** `FLASK_VAR`
        *   **Value:** Any (as you see fit)


### 3. Deploy the application to Render.com
1. Log in to your [Render.com](https://render.com/) dashboard
2. Click the `New` button, then select `Web Service`
3. Choose `Build and deploy from a Git repository` and connect your GitHub account
4. Select your repository (`devsecops-pipeline-prototype`) from the list
5. Configure the web service:
    *   **Name:** Give your service a name since Render will use this in the URL
    *   **Region:** Choose a geographic region close to you
    *   **Branch:** Make sure its set to `main` (or your primary dev branch)
    *   **Runtime:** Select `Docker` as Render should automatically detect your `Dockerfile`
    *   **Instance Type:** Choose the `Free` plan
    *   **Environment Variables:** This is important so that the application runs without issues
        *   Click `+ Add Environment Variable`
        *   Set the **Key** to `FLASK_VAR`.
        *   Set the **Value** to the **exact same secret key** you generated and added to GitHub secrets in Step 2
  
6. Click `Create Web Service`
7. Render will start building your Docker image and deploying the application
8. Once deployed, you will be provided with a public URL. Make sure to copy it

### 4. Update the pipeline configuration (OWASP ZAP)
OWASP ZAP scan needs to know the URL of your deployed application:
1. In your local repository or directly on GitHub, open the file `.github/workflows/pipeline.yaml`
2. Locate the `owasp-scan` job
3. Find the step named `OWASP ZAP Baseline Scan`
4. Under 'with:', update the `target:` value to the your public Render.com project's URL

Example:
```yaml
   owasp-scan:
     runs-on: ubuntu-latest
     needs: security-scans
     permissions:
       issues: write
     steps:
       - name: OWASP ZAP Baseline Scan
         uses: zaproxy/action-baseline@v0.14.0
         with:
           target: "YOUR URL HERE"
```
   
5. **Save** the changes to `pipeline.yaml`
6. **Commit and push** this update to your GitHub repository

### 5. SonarCloud configuration
SonarCloud requires additional configuration before running the pipeline.
1. Log in to [SonarCloud.io](https://sonarcloud.io/)
2. If not previously done before, import the repository as a project from GitHub
3. Navigate to the project dashboard
4. Press "Information" button on the left panel
5. Locate and save "Project Key" and "Organization Key" values
6. Navigate to the root of the repository directory and create a file `sonar-project.properties`
7. Type the first line `sonar.projectKey=` with your Project key followed
8. Type the second line `sonar.organization=` with your Organization key followed
9. Save the file

An example file of `sonar-project.properties`

```yaml
sonar.projectKey= your project key here
sonar.organization= your organization key here
```
   

## Running the pipeline
The GitHub Actions workflow in `pipeline.yaml` is configured to trigger automatically on every `push` event to the `main` branch

Simply pushing code changes will initiate a pipeline run. You can also trigger or re-run it manually from the Actions tab if needed

## Viewing scan results and reports
- **Pipeline execution:** Go to the `Actions` tab in your GitHub repository to view the live progress and logs of each job (build-test, security-scans, owasp-scan)
- **Unit Tests (Pytest):** Results are visible directly in the logs of the `build-test` job's "Run Pytest" step
- **SAST (SonarCloud):** Visit your dashboard on [SonarCloud.io](https://sonarcloud.io/) for a detailed analysis, but also a dedicated summary link is provided within the logs of 'security-scans', under `SonarCloud scan` step
- **SCA (Snyk):** Visit your project on [app.snyk.io](https://app.snyk.io/) to see detailed dependency vulnerabilities. A dedicated summary link can be accessed from the logs 'security-scans', under 'Snyk Scan' step
- **DAST (OWASP ZAP):** Scan results summary and logs are automatically created in 'Issues' tab of your repository. Additionally, an HTML report is available as an artifact from the 'Summary page' of each pipeline run