pipeline {
    agent any

    stages {
        stage("Install & Run Tests"){
            steps {
                bat 'python -m pip install requirements.txt'
                bat 'start /B python app.py'
                bat 'python -m pytest -v tests/test_demo'
            }
        }

        stage("Build Docker Image"){
            steps{
                bat 'docker build -t exam-img .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'exam-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PWD'
                )]) {
                    bat 'docker login -u "%USER%" -p "%PWD%"'
                }
            }
        }

        stage('Push Image') {
            steps {
                bat 'docker tag exam-repo:exam-img bavyaraghu/exam-repo:exam-img'
                bat 'docker push bavyaraghu/exam-repo:exam-img'
            }
        }


        stage('Deploy') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}



