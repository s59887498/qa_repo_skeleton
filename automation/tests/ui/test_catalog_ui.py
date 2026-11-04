import os

import pytest


@pytest.fixture
def driver():
    # Imports occur only when the opt-in UI lane runs. Missing dependencies then fail clearly.
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-dev-shm-usage")
    if os.environ.get("QA_CHROME_BINARY"):
        options.binary_location = os.environ["QA_CHROME_BINARY"]
    service = Service(os.environ["QA_CHROMEDRIVER"]) if os.environ.get("QA_CHROMEDRIVER") else Service()
    browser = webdriver.Chrome(service=service, options=options)
    try:
        yield browser
    finally:
        browser.quit()


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.case("UI-001", "由頁面建立項目並確認後端", steps=["填寫名稱", "建立", "讀回 API"], expected="UI 與 API 資料一致")
def test_create_item(driver, api, demo_url):
    from qa_demo.pages import CatalogPage
    page = CatalogPage(driver)
    page.open(demo_url)
    result = page.create("demo-from-ui")
    assert result.text == "已建立：demo-from-ui"
    item = api.request("GET", f"/items/{result.get_attribute('data-item-id')}")
    assert item.status_code == 200
    assert item.json()["name"] == "demo-from-ui"
