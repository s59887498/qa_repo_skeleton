"""Exercise real browser failure artifacts without leaving a failing case in the suite."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.ui
def test_playwright_retains_only_failed_artifacts(tmp_path, browser_name):
    for should_fail in (False, True):
        directory = tmp_path / ("failed" if should_fail else "passed")
        directory.mkdir()
        (directory / "conftest.py").write_text(
            (ROOT / "conftest.py").read_text() + "\n" +
            (ROOT / "automation/tests/ui/conftest.py").read_text(), encoding="utf-8"
        )
        (directory / "pytest.ini").write_text(
            "[pytest]\nmarkers =\n    case: synthetic case\n    ui: local browser example\n"
        )
        expected_text = "Synthetic mismatch" if should_fail else "Demo action"
        (directory / "test_example.py").write_text(
            "import pytest\nfrom playwright.sync_api import expect\n"
            "@pytest.mark.ui\n"
            "@pytest.mark.case('UICHECK-001', 'Synthetic browser', steps=['click'], expected='Demo action')\n"
            "def test_example(page):\n"
            "    assert page.viewport_size == {'width': 1440, 'height': 900}\n"
            "    page.set_content('<button>Demo action</button>')\n"
            "    button = page.get_by_role('button', name='Demo action')\n"
            "    button.click()\n"
            f"    expect(button).to_have_text({expected_text!r}, timeout=200)\n"
        )
        command = [
            sys.executable, "-m", "pytest", "-p", "playwright", "-q", "--run-ui",
            "--browser", browser_name, "--tracing", "retain-on-failure",
            "--screenshot", "only-on-failure", "--output", "browser-artifacts",
            "--results-json", "results.json",
        ]
        with_allure = importlib.util.find_spec("allure_pytest") is not None
        if with_allure:
            command += ["-p", "allure_pytest", "--alluredir", "allure"]
        result = subprocess.run(
            command, cwd=directory, capture_output=True, text=True, timeout=60,
            env={**os.environ, "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        )
        assert result.returncode == int(should_fail), result.stdout + result.stderr
        record = json.loads((directory / "results.json").read_text())
        assert record["ui"]["browser"] == browser_name
        assert record["results"][0]["browser"] == browser_name
        assert record["results"][0]["status"] == ("failed" if should_fail else "passed")
        traces = list((directory / "browser-artifacts").rglob("trace.zip"))
        screenshots = list((directory / "browser-artifacts").rglob("*.png"))
        assert len(traces) == len(screenshots) == int(should_fail)
        if should_fail:
            with zipfile.ZipFile(traces[0]) as trace:
                assert any(name.endswith(".trace") for name in trace.namelist())
            assert screenshots[0].read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        if with_allure:
            data = json.loads(next((directory / "allure").glob("*-result.json")).read_text())
            assert data["name"] == "UICHECK-001 Synthetic browser"
            assert data["status"] == ("failed" if should_fail else "passed")
