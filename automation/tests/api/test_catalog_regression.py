"""Group by feature; select smoke/regression independently of the environment."""

import json
from pathlib import Path

import pytest

pytestmark = [pytest.mark.api, pytest.mark.regression]
DATA = json.loads((Path(__file__).parents[2] / "data/catalog.json").read_text())


@pytest.mark.smoke
@pytest.mark.case("CAT-001", "服務健康檢查", steps=["呼叫健康檢查"], expected="回應 ok")
def test_health(api):
    response = api.request("GET", "/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.case("CAT-002", "建立讀取與清理項目", steps=["建立項目", "讀回", "清理並讀回"], expected="資料一致且清理後找不到")
def test_owned_item_lifecycle(api):
    response = api.request("POST", "/items", json={"name": "demo-item"}, headers={"X-Demo-Role": "editor"})
    assert response.status_code == 201
    item = response.json()
    try:
        found = api.request("GET", f"/items/{item['id']}")
        assert found.status_code == 200
        assert found.json() == item
        assert item["name"] == "demo-item"
    finally:
        cleaned = api.request("DELETE", f"/items/{item['id']}", headers={"X-Demo-Role": "editor"})
        assert cleaned.status_code == 200, "Owned cleanup failed"
        assert api.request("GET", f"/items/{item['id']}").status_code == 404


@pytest.mark.parametrize("role", [pytest.param(
    row["role"], id=row["case_id"], marks=pytest.mark.case(
        row["case_id"], row["title"], steps=["使用指定角色建立項目"], expected="回應 403"
    )) for row in DATA["denied_roles"]])
def test_denied_role_cannot_create(api, role):
    response = api.request("POST", "/items", json={"name": "demo-item"}, headers={"X-Demo-Role": role})
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}


@pytest.mark.parametrize("length, expected_status", [pytest.param(
    row["length"], row["status"], id=row["case_id"], marks=pytest.mark.case(
        row["case_id"], row["title"], steps=["送出指定長度的名稱"], expected=f"HTTP {row['status']}"
    )) for row in DATA["name_boundaries"]])
def test_name_length_boundary(api, length, expected_status):
    response = api.request("POST", "/items", json={"name": "x" * length}, headers={"X-Demo-Role": "editor"})
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["name"] == "x" * length
    else:
        assert response.json() == {"error": "invalid_name"}
