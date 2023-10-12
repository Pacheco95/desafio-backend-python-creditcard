import re

from fastapi.testclient import TestClient
from pytest import fixture
from starlette import status

from app.main import app

client = TestClient(app)


@fixture
def invalid_exp_date_card():
    return {
        "exp_date": "13/2026",
        "holder": "Fulano",
        "number": "0000000000000001",
        "cvv": "123",
    }


def test_create_card_endpoint_should_fail_exp_date(invalid_exp_date_card):
    response = client.post("/card", json=invalid_exp_date_card)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert re.match(r".*is not a valid date.*", response.text)
