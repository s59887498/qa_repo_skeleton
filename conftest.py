"""Local demos by default; optional lanes must be selected explicitly."""

from datetime import datetime, timezone
import json
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--run-ui", action="store_true", help="Run local Selenium examples")
    parser.addoption("--run-protocol", action="store_true", help="Run local WebSocket examples")
    parser.addoption("--run-live", action="store_true", help="Run configured live read-only tests")
    parser.addoption("--results-json", help="Write a machine-readable execution record")


def pytest_configure(config):
    config._qa_results = {}
    config._qa_started_at = datetime.now(timezone.utc).isoformat()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    # Apply after Allure's setup wrapper populates its default function-name title.
    yield
    marker = item.get_closest_marker("case")
    if not marker or not item.config.pluginmanager.hasplugin("allure_pytest"):
        return
    import allure
    case_id, title = marker.args
    allure.dynamic.id(case_id)
    allure.dynamic.title(f"{case_id} {title}")
    steps = "\n".join(f"{number}. {step}" for number, step in enumerate(marker.kwargs["steps"], 1))
    allure.dynamic.description(f"Steps\n{steps}\n\nExpected\n{marker.kwargs['expected']}")


def pytest_collection_modifyitems(config, items):
    seen = set()
    for item in items:
        for lane in ("ui", "protocol", "live"):
            if item.get_closest_marker(lane) and not config.getoption(f"--run-{lane}"):
                item.add_marker(pytest.mark.skip(reason=f"Opt-in lane: --run-{lane}"))
        marker = item.get_closest_marker("case")
        if not marker:
            if "/automation/tests/" in str(item.path):
                raise pytest.UsageError(f"Missing case metadata: {item.nodeid}")
            continue
        case_id, title = marker.args
        if case_id in seen:
            raise pytest.UsageError(f"Duplicate case ID: {case_id}")
        if not title or not marker.kwargs.get("steps") or not marker.kwargs.get("expected"):
            raise pytest.UsageError(f"Incomplete case metadata: {case_id}")
        seen.add(case_id)
        item.user_properties.extend([("case_id", case_id), ("title", title)])
        config._qa_results[item.nodeid] = {
            "case_id": case_id, "title": title, "status": "not_run",
            "actual": "Not executed", "evidence": [],
            "lane": next((lane for lane in ("live", "ui", "protocol") if item.get_closest_marker(lane)), "local"),
        }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    result = item.config._qa_results.get(item.nodeid)
    if result is None:
        return
    # Setup and teardown failures must override a passing call.
    if report.failed:
        result["status"] = "failed"
        result["actual"] = f"{report.when} failed; inspect restricted JUnit / console evidence"
    elif report.skipped and result["status"] != "failed":
        result["status"] = "skipped"
        result["actual"] = "Skipped; see pytest skip reason"
    elif report.when == "call" and report.passed and result["status"] != "failed":
        result["status"] = "passed"
        result["actual"] = "Assertions passed"
    result["evidence"] = [item.nodeid]


def pytest_sessionfinish(session, exitstatus):
    destination = session.config.getoption("--results-json")
    if not destination:
        return
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "schema_version": 1, "scope": "run", "environment": "see per-case lane",
        "started_at": session.config._qa_started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": int(exitstatus),
        "results": list(session.config._qa_results.values()),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
