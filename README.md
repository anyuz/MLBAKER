# MLBAKER
This is a pipeline of baking Jenkins to K8s to dynamic allocate training pods for different ML models

# What MLBaker can do?
##  This is a simple demo to show how the MLbaker works 

https://drive.google.com/open?id=1HlnlsjRgCrWFRWUZP828Wjwmx03Cp0yU


##  Architecture

![Architecture](archi.png)


## Jenkinsfile to Dynamic Allocate K8s Training Pod



pipeline {

    agent {
        kubernetes {
        label 'jenkins-slave'
        defaultContainer 'jnlp'
        yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: some-label-value
spec:
  volumes:
  - name: traindata
    persistentVolumeClaim:
      claimName: traindata
  containers:
  - name: python
    image: python:3.7.2-slim
    volumeMounts:
    - name: traindata
      mountPath: /data
    env:
    - name: MONGODB_URL
      valueFrom:
        secretKeyRef:
          key: mongodb
          name: db-user-pass
    - name: MONGODB_USER
      valueFrom:
        secretKeyRef:
          key: user
          name: db-user-pass
    - name: MONGODB_PASSWORD
      valueFrom:
        secretKeyRef:
          key: password
          name: db-user-pass
    - name: AWS_ACCESS_KEY_ID
      valueFrom:
        secretKeyRef:
          key: AWS_ACCESS_KEY_ID
          name: s3reader
    - name: AWS_SECRET_ACCESS_KEY
      valueFrom:
        secretKeyRef:
          key: AWS_SECRET_ACCESS_KEY
          name: s3reader
    command:
    - cat
    tty: true
"""
        }
    }

  
    stages{
        stage('Download requirements'){
            steps{
                container('python'){
                    sh 'apt update'
                    sh 'apt install libgomp1'
                    sh 'pip install -r requirements.txt'
                    sh 'pip install -U pytest'
                }
            }
        }
        stage('pytest') {
            steps{
                container('python'){
                    sh 'py.test update.py --junitxml=pytest_report.xml'
                }
            }
        }
        stage('Run model') {
            steps{
                container('python'){
                    sh 'python model.py --mongodb ${MONGODB_URL} --user ${MONGODB_USER} --password ${MONGODB_PASSWORD} --datapath /data'
                }
            }
        }
        
        stage('accuracy-test'){
            steps{
                container('python'){
                    sh 'py.test accuracy.py --junitxml=pytest_report.xml'
                }
            }
        }
    }
}
