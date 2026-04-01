pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-api"
        CONTAINER_NAME = "inventory-api-container"
    }

    stages {

        stage('Clone from GitHub') {
            steps {
                checkout scm
            }
        }

        stage('Create .env file') {
            steps {
                bat '''
                echo MONGO_URI=mongodb+srv://b00157129_db_user:Bula2cao@cluster0.lioc5vj.mongodb.net/?appName=Cluster0>.env
                echo DB_NAME=inventory_db>>.env
                echo COLLECTION_NAME=products>>.env
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Docker Container in Background') {
            steps {
                bat '''
                docker rm -f %CONTAINER_NAME% 2>nul
                docker run -d --name %CONTAINER_NAME% -p 8000:8000 %IMAGE_NAME%
                '''
            }
        }

        stage('Wait for API to Start') {
            steps {
                powershell 'Start-Sleep -Seconds 10'
            }
        }

        stage('Install Newman') {
            steps {
                bat 'npm install -g newman'
            }
        }

        stage('Run Postman Tests with Newman') {
            steps {
                bat 'npx newman run postman_collection.json'
            }
        }

        stage('Generate README.txt') {
            steps {
                bat 'py scripts\\generate_readme.py'
            }
        }

        stage('Create Final Zip') {
            steps {
                bat '''
                powershell -Command "$dt=Get-Date -Format 'yyyy-MM-dd-HH-mm'; Compress-Archive -Path main.py,database.py,models.py,requirements.txt,Dockerfile,Jenkinsfile,README.txt,scripts,postman_collection.json -DestinationPath complete-$dt.zip -Force"
                '''
            }
        }
    }

    post {
        always {
            bat 'docker rm -f %CONTAINER_NAME% 2>nul'
            archiveArtifacts artifacts: '*.zip, README.txt', fingerprint: true
        }
    }
}