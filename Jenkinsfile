pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO_URI = '992382545251.dkr.ecr.us-east-1.amazonaws.com/danielrubin/catnip'
        IMAGE_TAG = 'latest'
        EC2_INSTANCE_IP = '54.147.46.142'  // Replace with your EC2 public IP
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

        stage('Deploy to EC2') {
            steps {
                script {
                    sh '''
                    # SSH into EC2 instance and run the Docker container with port 80 exposed
                    ssh -o StrictHostKeyChecking=no -i ~/sshkey ubuntu@$EC2_INSTANCE_IP << 'EOF'
                    # Pull the Docker image from ECR
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI
                    docker pull $ECR_REPO_URI:$IMAGE_TAG

                    # Run the container with port 80 exposed
                    docker run -d -p 80:80 --name catnip-container $ECR_REPO_URI:$IMAGE_TAG
                    EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Image pushed to ECR and deployed to EC2 successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
