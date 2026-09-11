pipeline {
    agent any
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
        stage('Quality Checks') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        echo "Running unit tests"
                        sh """
                            . ${VENV_DIR}/bin/activate
                            pytest -v --tb=short
                        """
                    }
                }
                stage('Syntax Check') {
                    steps {
                        echo "Checking Python Syntax"
                        sh """
                            . ${VENV_DIR}/bin/activate
                            ${PYTHON} -m py_compile app.py homepage.py jobs.py auth.py
                        """
                        echo 'All files syntax OK'
                    }
                }
            }
        }
        stage('Deploy Info') {
            when {
                allOf {
                    expression { params.BUILD_ENV != 'prod' }
                    expression {env.GIT_BRANCH == '/origin/main/' || env.GIT_BRANCH == 'main'}
                }
            }
            steps {
                echo "Deploying ${APP_NAME}-${BUILD_NUMBER} to ${params.BUILD_ENV}"
                echo "Build tag: ${APP_NAME}:${GIT_COMMIT.take(7)}"
            }
        }
        stage('Prod Gate'){
            when {
                allOf {
                    expression { params.BUILD_ENV == 'prod' }
                }
            }
            steps {
                echo 'Production deployment requires manual approval'
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