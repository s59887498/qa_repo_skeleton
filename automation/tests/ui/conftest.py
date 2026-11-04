"""Use plugin-managed contexts so CLI tracing/screenshots and isolation stay effective."""

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1440, "height": 900}}


@pytest.fixture
def catalog_page(page):
    # Lazy import keeps the core (non-UI) install usable without Playwright.
    from qa_demo.pages import CatalogPage
    page.set_default_timeout(5000)
    page.set_default_navigation_timeout(10000)
    return CatalogPage(page)
