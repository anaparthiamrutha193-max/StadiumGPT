from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_register_validation():
    response = client.post(
        "/auth/register",
        json={}
    )

    assert response.status_code == 422


def test_login_validation():
    response = client.post(
        "/auth/login"
    )

    assert response.status_code in [401, 422]