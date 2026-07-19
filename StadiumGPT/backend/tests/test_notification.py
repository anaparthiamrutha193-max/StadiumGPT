from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_notifications_without_login():
    response = client.get("/notifications")

    assert response.status_code == 401