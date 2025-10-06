import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_me(client):
    payload = {"name": "Apple", "price": 1.99}
    response = client.post("/items/", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"item_name": "Apple", "item_price": 1.99}


