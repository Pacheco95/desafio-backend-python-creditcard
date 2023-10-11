from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"status": "RUNNING"}
