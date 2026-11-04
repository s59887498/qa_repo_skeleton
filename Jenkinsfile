pipeline {
    agent any
    options { timeout(time: 15, unit: 'MINUTES') }
    stages {
        stage('Install') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -e ".[dev,documents,protocol]"'
            }
        }
        stage('Validate') {
            steps {
                sh '.venv/bin/python scripts/check_template.py'
                sh '.venv/bin/ruff check .'
            }
        }
        stage('Local regression') {
            steps {
                sh '.venv/bin/python -m pytest --run-protocol --junitxml=artifacts/junit.xml --results-json=artifacts/results.json'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'artifacts/junit.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'artifacts/**'
        }
    }
}
