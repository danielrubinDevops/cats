pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO_URI = '992382545251.dkr.ecr.us-east-1.amazonaws.com/danielrubin/catnip'
        IMAGE_TAG = 'latest'
        REMOTE_SERVER = 'ubuntu@192.168.2.70' // SSH target server
        SSH_KEY_PATH = '~/sshkey'  // Path to your SSH private key
    }

    stages {
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
                    docker build -t $ECR_REPO_URI:$IMAGE_TAG -f ./flask-app/Dockerfile ./flask-app
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

        stage('Deploy to Remote Server') {
            steps {
                script {
                    sh """
                    ssh -i $SSH_KEY_PATH $REMOTE_SERVER '
                    echo "Pulling Docker image from ECR and starting container on remote server"
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI
                    docker pull $ECR_REPO_URI:$IMAGE_TAG
                    docker stop catnip-container || true
                    docker rm catnip-container || true
                    docker run -d -p 80:5000 --name catnip-container $ECR_REPO_URI:$IMAGE_TAG
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Image pushed to ECR and deployed to remote server successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
