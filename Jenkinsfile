pipeline {
    agent any
    environment {
        APP_NAME = 'jobportal'
        PYTHON = 'python3'
    }
    stages {
        stage('Checkout') {
            steps {
                echo "Building ${APP_NAME} - Build #${BUILD_NUMBER}"
                echo "Branch : ${GIT_BRANCH}"
                echo "Commit : ${GIT_COMMIT}"
                sh 'ls -la'
            }
        }
        stage('Install') {
            steps {
                echo "Installing dependencies from requirements.txt"
                sh '${PYTHON} -m pip install --upgrade pip'
                sh '${PYTHON} -m pip install -r requirements.txt'
                sh '${PYTHON} -m pip list'
            }
        }
        stage('Test') {
            steps {
                echo "Running tests suite"
                sh '${PYTHON} -m pytest -v --tb=short'
            }
        }
    }
    post {
        always {
            echo "Pipeline finished - Result: $(currentBuild.result)"
        }
        success {
            echo 'All tests passed — JobPortal is healthy'
        }
        failure {
            echo 'Pipeline failed — check console output above'
        }
    }
}