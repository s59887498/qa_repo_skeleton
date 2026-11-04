import pytest

from qa_demo.client import LiveSettings
from qa_demo.load import meets_thresholds, percentile, run_load
from qa_demo.server import demo_server


def test_empty_live_settings_never_fall_back_to_another_environment(monkeypatch):
    monkeypatch.delenv("QA_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="explicit"):
        LiveSettings.from_env()


@pytest.mark.parametrize("url", ["https://user:pass@example.invalid", "https://example.invalid/?token=x"])
def test_credentials_are_not_accepted_in_urls(monkeypatch, url):
    monkeypatch.setenv("QA_BASE_URL", url)
    with pytest.raises(ValueError, match="credentials"):
        LiveSettings.from_env()


def test_token_is_never_in_settings_repr():
    assert "synthetic-secret" not in repr(LiveSettings("https://example.invalid", "synthetic-secret"))


def test_insecure_live_token_transport_is_rejected(monkeypatch):
    monkeypatch.setenv("QA_BASE_URL", "http://example.invalid")
    monkeypatch.setenv("QA_API_TOKEN", "synthetic-secret")
    with pytest.raises(ValueError, match="HTTPS"):
        LiveSettings.from_env()


@pytest.mark.parametrize("mode", ["staggered", "simultaneous"])
def test_load_covers_every_synthetic_request_once(mode):
    with demo_server() as url:
        result = run_load(url, count=12, workers=3, mode=mode, ramp_interval=0)
    assert [s["sequence"] for s in result["samples"]] == list(range(12))
    assert result["failures"] == 0
    assert result["requests"] == 12


def test_load_records_failed_requests_and_fails_gate():
    with demo_server() as url:
        result = run_load(url, count=4, workers=2, path="/missing", ramp_interval=0)
    assert result["failures"] == 4
    assert result["error_rate"] == 1
    assert not meets_thresholds(result, p95_ms=10000, error_rate=0)
    assert all(s["status"] == 404 for s in result["samples"])


def test_load_refuses_remote_targets():
    with pytest.raises(ValueError, match="loopback"):
        run_load("https://example.invalid")


def test_percentile_and_latency_gate():
    assert percentile(list(range(1, 101)), 95) == 95
    assert not meets_thresholds({"requests": 10, "p95_ms": 501, "error_rate": 0}, p95_ms=500, error_rate=0)
