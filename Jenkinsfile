pipeline {
    agent any
    tools {
        maven 'Maven-3'
    }
    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timestamps()
    }
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
        PYTHON   = 'python3'
        VENV_DIR = 'venv'
        GITHUB_TOKEN = credentials('github-pat')
    }
    stages {
        stage('Checkout') {
            steps {
                echo "=== ${APP_NAME} | Build #${BUILD_NUMBER} | ${params.BUILD_ENV} ==="
                echo "Environment: ${params.BUILD_ENV}"
                echo "Branch : ${env.GIT_BRANCH}"
                echo "Commit : ${env.GIT_COMMIT}"
                sh "ls -la"
                sh "git log --oneline -3"
                sh "${PYTHON} --version"
            }
        }
        stage('Python : Install') {
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
        stage('Python : Test') {
            stage() {
                echo 'Running Python tests'
                sh '${PYTHON} -m pytest -v --tb=short'
            }
        }
        stage('Maven : Build') {
            steps {
                echo 'Building Java application with Maven'
                dir('hello-java') {
                    sh 'mvn clean package'
                    sh 'ls -lh target/*.jar'
                }
            }
        }
        stage('Maven : Test Results') {
            steps {
                dir('hello-java') {
                    echo 'Maven Tests Completed'
                    sh 'cat target/surefire-reports/*.txt 2>/dev/null || echo No surefire txt reports'
                }
            }
        }
    }
    post {
        always {
            echo "=== Build #${BUILD_NUMBER} complete: ${currentBuild.currentResult} ==="
            cleanWs()
        }
        success {
            echo "SUCCESS — ${APP_NAME} CI passed on ${params.BUILD_ENV}"
        }
        failure {
            echo "FAILURE — check Build #${BUILD_NUMBER} console output"
        }
        fixed {
            echo 'Pipeline recovered — was broken, now passing'
        }
        regression {
            echo 'Pipeline regressed — was passing, now broken'
        }
    }
}