import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)


def test_user_me(client):
    response = client.get("/agenticai/api/v1/user/me")
    assert response.status_code == 200
    assert response.json() == {"user_id": "the current user test pipeline"}

def test_user_login(client):
    response = client.get("/agenticai/api/v1/user/login")
    assert response.status_code == 200
    assert response.json() == {"user_id": "the current user login  "}


