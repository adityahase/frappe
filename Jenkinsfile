pipeline {
  agent any
  stages {
    stage('Sanity Test') {
      steps {
        sh 'python3 -v'
        sh 'pwd'
        sh 'whoami'
        sh 'ls /'
        sh 'ls /root'
        sh 'cat /home/frappe/.ssh/id_rsa.pub'
      }
    }
  }
}