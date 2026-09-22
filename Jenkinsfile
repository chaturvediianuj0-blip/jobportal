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
            name: 'SKIP_SONAR',
            defaultValue: false,
            description: 'Skip SonarQube analysis (emergency only)'
        )
    }
    environment {
        APP_NAME = 'jobportal'
        PYTHON   = 'python3'
        VENV_DIR = 'venv'
        GITHUB_TOKEN = credentials('github-pat')
        SONAR_TOKEN = credentials('sonar-token-hello-java')
    }
    stages {
        stage('Checkout') {
            steps {
                echo "=== ${APP_NAME} | Build #${BUILD_NUMBER} | ${params.BUILD_ENV} ==="
                echo "Environment: ${params.BUILD_ENV}"
                echo "Branch : ${env.GIT_BRANCH}"
                echo "Commit : ${env.GIT_COMMIT}"
                sh "${PYTHON} --version"
                sh "mvn -version"
                sh "sonar-scanner --version"
            }
        }
        stage('Python : Install') {
            steps {
                echo "Creating virtual environment and installing dependencies"
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt -q
                """
            }
        }
        stage('Python : Test') {
            steps {
                echo 'Running Python tests suite'
                sh """
                    . ${VENV_DIR}/bin/activate
                    pytest -v --tb=short --junit-xml=junit-report.xml --cov=. --cov-report=xml:coverage.xml
                    """
            }
        }
        stage('Sonarqube: Python') {
            when {
                expression { !params.SKIP_SONAR }
            }
            steps {
                echo 'Running SonarQube analysis for Python code'
                withSonarQubeEnv('SonarQube') {
                    sh """
                        . ${VENV_DIR}/bin/activate
                        /opt/sonar-scanner/bin/sonar-scanner \
                            -Dsonar.projectKey=hello-java \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.token=${SONAR_TOKEN}
                    """
                }
            }
        }
        stage('Quality Gate: Python') {
            when {
                expression { !params.SKIP_SONAR }
            }
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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
        stage('Maven : SonarQube') {
            when {
                expression { !params.SKIP_SONAR }
            }
            steps {
                echo 'Running SonarQube analysis on Java code'
                dir('hello-java') {
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            mvn sonar:sonar \
                                -Dsonar.projectKey=hello-java \
                                -Dsonar.host.url=http://localhost:9000 \
                                -Dsonar.token=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }
        stage('Maven : Deploy to Nexus') {
            steps {
                echo 'Deploying artifact to Nexus'
                dir('hello-java') {
                    sh 'mvn deploy -DskipTests'
                    echo "Deployed: hello-java-${BUILD_NUMBER} to Nexus"
                }
            }
        }
        stage('Summary') {
            steps {
                echo "=== Build #${BUILD_NUMBER} Summary ==="
                echo "App      : ${APP_NAME}"
                echo "Env      : ${params.BUILD_ENV}"
                echo "Branch   : ${GIT_BRANCH}"
                echo "Commit   : ${GIT_COMMIT.take(7)}"
                echo "Artifact : hello-java-1.0-SNAPSHOT.jar in Nexus"
                echo "Quality  : ${params.SKIP_SONAR ? 'Skipped' : 'Completed'}"
            }
        }
    }
    post {
        always {
            echo "Build #${BUILD_NUMBER} result: ${currentBuild.currentResult}"
            junit allowEmptyResults: true, testResults: 'junit-report.xml'
            junit allowEmptyResults: true, testResults: 'hello-java/target/surefire-reports/*.xml'
            cleanWs()
        }
        success {
            echo "SUCCESS — ${APP_NAME} pipeline complete on ${params.BUILD_ENV}"
        }
        failure {
            echo "FAILURE — check Build #${BUILD_NUMBER} console and SonarQube"
        }
        fixed {
            echo 'Pipeline recovered — was broken, now passing'
        }
        regression {
            echo 'Pipeline regressed — was passing, now broken'
        }
    }
}