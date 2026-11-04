"""Exercise the actual pytest hooks, especially cleanup failures after a passing call."""

import json
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("fixture_code, test_code, expected, exit_code", [
    ("yield\n    raise RuntimeError('cleanup failed')", "assert True", "failed", 1),
    ("raise RuntimeError('setup failed')\n    yield", "assert True", "failed", 1),
    ("yield", "pytest.skip('synthetic exclusion')", "skipped", 0),
])
def test_execution_record_keeps_nonpassing_phases(tmp_path, fixture_code, test_code, expected, exit_code):
    (tmp_path / "conftest.py").write_text((ROOT / "conftest.py").read_text())
    (tmp_path / "pytest.ini").write_text("[pytest]\nmarkers =\n    case: synthetic case\n")
    (tmp_path / "test_example.py").write_text(
        "import pytest\n@pytest.fixture\ndef resource():\n    " + fixture_code +
        "\n@pytest.mark.case('DEMO-001', 'Synthetic', steps=['run'], expected='complete')\n" +
        "def test_result(resource):\n    " + test_code + "\n"
    )
    command = [sys.executable, "-m", "pytest", "-q", "--results-json=result.json"]
    with_allure = importlib.util.find_spec("allure_pytest") is not None
    if with_allure:
        command += ["-p", "allure_pytest", "--alluredir=allure"]
    result = subprocess.run(
        command,
        cwd=tmp_path, capture_output=True, text=True, timeout=30,
        env={**os.environ, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
    )
    assert result.returncode == exit_code, result.stdout
    report = json.loads((tmp_path / "result.json").read_text())
    assert report["results"][0]["status"] == expected
    assert report["exit_code"] == exit_code
    if with_allure:
        allure_result = json.loads(next((tmp_path / "allure").glob("*-result.json")).read_text())
        assert allure_result["name"] == "DEMO-001 Synthetic"
        assert "Expected" in allure_result["description"]
