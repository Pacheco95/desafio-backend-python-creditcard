import re
from datetime import datetime
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from pytest import fixture
from starlette import status

from app.main import app
from app.utils.datetime import as_utc

client = TestClient(app)


@fixture
def invalid_exp_date_card():
    return {
        "exp_date": "13/2026",
        "holder": "Fulano",
        "number": "0000000000000001",
        "cvv": "123",
    }


@fixture
def invalid_exp_date_expired(invalid_exp_date_card):
    return {
        **invalid_exp_date_card,
        "exp_date": "01/3000",
    }


def test_create_card_endpoint_should_fail_exp_date(invalid_exp_date_card):
    response = client.post("/card", json=invalid_exp_date_card)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert re.match(r".*is not a valid date.*", response.text)


@patch("app.business.validators.utcnow")
def test_create_card_endpoint_should_fail_expired(mock_utcnow: MagicMock, invalid_exp_date_expired):
    mock_utcnow.return_value = as_utc(datetime.fromisoformat("4000-01-01"))
    response = client.post("/card", json=invalid_exp_date_expired)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert re.match(r".*already expired.*", response.text)
