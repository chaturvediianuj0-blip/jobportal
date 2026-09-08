pipeline {
    agent any
    environment {
        APP_NAME = 'jobportal'
        VENV_DIR = 'venv'
    }
    stages {
        stage('Checkout') {
            steps {
                echo "Building ${env.APP_NAME} - Build #${env.BUILD_NUMBER}"
                echo "Branch : ${env.GIT_BRANCH}"
                echo "Commit : ${env.GIT_COMMIT}"
                sh "ls -la"
            }
        }
        stage('Install') {
            steps {
                echo "Creating virtual environment and installing dependencies"
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list
                """
            }
        }
        stage('Test') {
            steps {
                echo "Running test suite inside virtual environment"
                sh """
                    . ${VENV_DIR}/bin/activate
                    pytest -v --tb=short
                """
            }
        }
    }
    post {
        always {
            echo "Pipeline finished - Result: ${currentBuild.currentResult}"
        }
        success {
            echo 'All tests passed — JobPortal is healthy'
        }
        failure {
            echo 'Pipeline failed — check console output above'
        }
    }
}