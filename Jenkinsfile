pipeline {
  agent any
  stages {
    stage('Install') {
      steps {
        dockerNode(image: 'python:3.7') {
          sh 'whoami'
        }

      }
    }

  }
}