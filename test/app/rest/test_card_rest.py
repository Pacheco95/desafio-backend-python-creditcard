from fastapi.testclient import TestClient
from starlette import status

from app.main import app

client = TestClient(app)


def test_create_card_endpoint_should_fail_exp_date():
    invalid_card = {
        "exp_date": "02/2026",
        "holder": "Fulano",
        "number": "0000000000000001",
        "cvv": "123",
    }
    response = client.post("/card", json=invalid_card)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
