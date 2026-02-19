from fastapi.testclient import TestClient
import improved_app

client = TestClient(improved_app.app)

def setup_function():
    improved_app.items.clear()
    improved_app.items.update({1: {"name": "apple", "price": 1.2}})

def test_improved_missing_name_returns_standard_validation_error():
    r = client.post("/items", json={"price": 2})
    assert r.status_code == 422
    body = r.json()
    assert body["error_code"] == "VALIDATION_ERROR"
    assert "details" in body
    assert any(d.get("field") == "name" for d in body["details"])

def test_improved_extra_field_forbidden_returns_standard_validation_error():
    r = client.post("/items", json={"name": "pear", "price": 2, "unknown": 123})
    assert r.status_code == 422
    body = r.json()
    assert body["error_code"] == "VALIDATION_ERROR"

def test_improved_not_found_returns_standard_app_error():
    r = client.get("/items/999")
    assert r.status_code == 404
    body = r.json()
    assert body["error_code"] == "ITEM_NOT_FOUND"
