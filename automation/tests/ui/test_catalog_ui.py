import pytest


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.case("UI-001", "由頁面建立項目並確認後端", steps=["填寫名稱", "建立", "讀回 API"], expected="UI 與 API 資料一致")
def test_create_item(catalog_page, api, demo_url):
    from playwright.sync_api import expect
    catalog_page.open(demo_url)
    result = catalog_page.create("demo-from-ui")
    expect(result).to_have_text("已建立：demo-from-ui")
    item_id = result.get_attribute("data-item-id")
    assert item_id, "Successful UI creation must expose the created item ID"
    item = api.request("GET", f"/items/{item_id}")
    assert item.status_code == 200
    assert item.json()["name"] == "demo-from-ui"
