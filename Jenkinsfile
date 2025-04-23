pipeline {
  agent any

  environment {
    SONARQUBE_SERVER = 'sonarqube'
    SONAR_SCANNER_HOME = 'C:\\sonarqube\\sonarqube-25.4.0.105899\\bin\\windows-x86-64'  // Cambia esto a la ruta real en tu Windows
    VENV = "${WORKSPACE}\\venv"
  }

  stages {
    stage('Check Python Version') {
      steps {
        bat '"C:\\Users\\jhone\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
      }
    }

    stage('Clonar repositorio') {
      steps {
        git branch: 'main', url: 'https://github.com/Jhon98E/practica-CI-CD.git'
      }
    }

    stage('Instalar dependencias') {
      steps {
        bat """
          "C:\\Users\\jhone\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv %VENV%
          call %VENV%\\Scripts\\activate.bat
          "%VENV%\\Scripts\\pip.exe" install --upgrade pip
          "%VENV%\\Scripts\\pip.exe" install -r requirements.txt
        """
      }
    }

    stage('Pruebas unitarias') {
      steps {
        bat """
          call %VENV%\\Scripts\\activate.bat
          "%VENV%\\Scripts\\pytest.exe" --maxfail=1 --disable-warnings --quiet
        """
      }
    }

    stage('Construir imagen Docker') {
      steps {
        script {
          dockerImage = docker.build("jhonenriquez2598/practica-cd")
        }
      }
    }

    stage('Login to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          bat """
            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% -p %DOCKER_PASS%
          """
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        script {
          docker.image('jhonenriquez2598/practica-cd').push()
        }
      }
    }

    stage('Lint') {
      steps {
        bat """
          call %VENV%\\Scripts\\activate.bat
          pip install pylint
          pylint src --output-format=json > pylint-report.json || exit 0
        """
      }
    }
  }
}
