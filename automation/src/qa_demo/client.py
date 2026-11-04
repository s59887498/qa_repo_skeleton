"""Explicit settings, bounded timeouts, and no payload logging."""

from dataclasses import dataclass, field
import math
import os
from urllib.parse import urlsplit

import requests


@dataclass(frozen=True)
class LiveSettings:
    base_url: str
    token: str = field(default="", repr=False)
    timeout: float = 5.0

    @classmethod
    def from_env(cls):
        url = os.environ.get("QA_BASE_URL", "").rstrip("/")
        parsed = urlsplit(url)
        if parsed.scheme not in {"https", "http"} or not parsed.hostname:
            raise ValueError("QA_BASE_URL must be an explicit http(s) URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("QA_BASE_URL must not contain credentials, query, or fragment")
        token = os.environ.get("QA_API_TOKEN", "")
        if token and parsed.scheme != "https":
            raise ValueError("Live credentials require HTTPS")
        timeout = float(os.environ.get("QA_TIMEOUT_SECONDS", "5"))
        if not math.isfinite(timeout) or not 0 < timeout <= 60:
            raise ValueError("QA_TIMEOUT_SECONDS must be between 0 and 60")
        return cls(url, token, timeout)


class ApiClient:
    def __init__(self, base_url, *, timeout=5.0, token=""):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.trust_env = False
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def request(self, method, path, **kwargs):
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("Use an absolute path within the configured origin")
        return self.session.request(
            method, self.base_url + path, timeout=self.timeout, allow_redirects=False, **kwargs
        )

    def close(self):
        self.session.close()
