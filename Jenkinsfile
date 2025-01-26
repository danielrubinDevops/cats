pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1' // Set your AWS region
        ECR_REPO_URI = '992382545251.dkr.ecr.us-east-1.amazonaws.com/danielrubin/catnip'
        IMAGE_TAG = 'latest' // Or use something like `env.BUILD_NUMBER` for versioning
        DOCKERFILE_PATH = './flaskapp/Dockerfile' // Specify the Dockerfile path
        CONTEXT_DIR = './flaskapp' // Specify the build context directory
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/danielrubinDevops/cats.git'
            }
        }

        stage('Authenticate with ECR') {
            steps {
                script {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                    docker build -t $ECR_REPO_URI:$IMAGE_TAG -f $DOCKERFILE_PATH $CONTEXT_DIR
                    '''
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    sh '''
                    docker push $ECR_REPO_URI:$IMAGE_TAG
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Image pushed to ECR successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
