"""Adapt /health only after checking the new project's published contract."""

import pytest

from qa_demo.client import ApiClient, LiveSettings


@pytest.mark.live
@pytest.mark.api
@pytest.mark.case("LIVE-001", "已設定環境健康檢查", steps=["讀取健康檢查端點"], expected="HTTP 200")
def test_configured_health():
    settings = LiveSettings.from_env()  # Missing settings FAIL an explicitly requested live run.
    client = ApiClient(settings.base_url, timeout=settings.timeout, token=settings.token)
    try:
        assert client.request("GET", "/health").status_code == 200
    finally:
        client.close()
