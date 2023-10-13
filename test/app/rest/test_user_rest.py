from fastapi.testclient import TestClient
from starlette import status

from app.main import app

client = TestClient(app)


def test_should_fail_create_duplicated_users():
    user = dict(username="John Doe", password="supersecret")
    response = client.post("/users", json=user)
    assert response.status_code == status.HTTP_201_CREATED, response.text

    response = client.post("/users", json=user)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    assert "already exists" in response.text
