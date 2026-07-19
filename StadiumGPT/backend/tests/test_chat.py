from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_chat_without_token():
    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code == 401


def test_chat_history_without_token():
    response = client.get("/chat/history")

    assert response.status_code == 401