pipeline {
    agent any
    options { timeout(time: 15, unit: 'MINUTES') }
    stages {
        stage('Install') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -e ".[dev,documents,protocol,ui,reports]"'
                // Provision Linux OS libraries on the agent separately: playwright install-deps chromium.
                sh '.venv/bin/python -m playwright install chromium'
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
        stage('Playwright UI') {
            steps {
                sh '''.venv/bin/python -m pytest automation/tests/ui tests/test_playwright_integration.py \
                    --run-ui --browser chromium --tracing retain-on-failure --screenshot only-on-failure \
                    --output artifacts/ui/chromium/playwright --junitxml=artifacts/ui/chromium/junit.xml \
                    --results-json=artifacts/ui/chromium/results.json --alluredir=artifacts/ui/chromium/allure-results'''
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'artifacts/**/junit.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'artifacts/**'
        }
    }
}
