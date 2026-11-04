import pytest

from qa_demo.client import ApiClient
from qa_demo.server import demo_server


@pytest.fixture
def demo_url():
    # Function scope isolates storage and cleanup across cases and parallel workers.
    with demo_server() as url:
        yield url


@pytest.fixture
def api(demo_url):
    client = ApiClient(demo_url)
    try:
        yield client
    finally:
        client.close()
