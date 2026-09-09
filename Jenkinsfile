pipeline {
    agent any
    parameters {
        choice(
            name: 'BUILD_ENV', 
            choices: ['dev', 'staging', 'prod'], 
            description: 'Target environment for this build'
        )
        booleanParam(
            name: 'RUN_FULL_TESTS', 
            defaultValue: true, 
            description: 'Run all tests (uncheck to skip slow tests)'
        )
    }
    environment {
        APP_NAME = 'jobportal'
        VENV_DIR = 'venv'
    }
    stages {
        stage('Checkout') {
            steps {
                echo "=== ${APP_NAME} Build #${BUILD_NUMBER} ==="
                echo "Environment: ${params.BUILD_ENV}"
                echo "Branch : ${env.GIT_BRANCH}"
                echo "Commit : ${env.GIT_COMMIT}"
                sh "ls -la"
                sh 'git log --oneline -3'
                sh '${PYTHON} --version'
            }
        }
        stage('Install') {
            steps {
                echo "Creating virtual environment and installing dependencies"
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip -q
                    pip install -r requirements.txt -q
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
        stage('Deploy Info') {
            when {
                expression {  params.BUILD_ENV == 'dev' }
            }
            steps {
                echo "Would deploy to DEV environment here"
                echo "Build tag: ${APP_NAME}-${BUILD_NUMBER}"
            }
        }
    }
    post {
        always {
            echo "Build #${BUILD_NUMBER} finished - Result: ${currentBuild.currentResult}"
        }
        success {
            echo "SUCCESS - ${APP_NAME} is healthy on ${params.BUILD_ENV} environment"
        }
        failure {
            echo "FAILURE — check console output for Build #${BUILD_NUMBER}"
        }
    }
}