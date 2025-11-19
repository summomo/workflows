import pytest
from app import app, items

@pytest.fixture

def client():
    app.config["TESTING"] = True
    items.clear()
    with app.test_client() as client:
        yield client

def test_index_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200

def test_add_item(client):
    resp = client.post("/add", data={"item": "Milk"})
    assert resp.status_code in (302, 303)
    assert items == ["Milk"]