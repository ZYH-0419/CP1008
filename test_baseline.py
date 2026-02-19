from fastapi.testclient import TestClient
import baseline_app

client = TestClient(baseline_app.app)

def setup_function():
    baseline_app.items.clear()
    baseline_app.items.update({1: {"name": "apple", "price": 1.2}})

def test_baseline_missing_name_is_400_string_detail():
    r = client.post("/items", json={"price": 2})
    assert r.status_code == 400
    # detail is a string here
    assert isinstance(r.json()["detail"], str)

def test_baseline_missing_price_is_400_dict_detail():
    r = client.post("/items", json={"name": "pear"})
    assert r.status_code == 400
    # detail is a dict here (inconsistent)
    assert isinstance(r.json()["detail"], dict)
