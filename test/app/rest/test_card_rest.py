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
def valid_visa_card():
    return {
        "exp_date": "10/2025",
        "holder": "Fulano da Silva",
        "number": "4220036484096326",
        "cvv": "606",
    }


@fixture
def invalid_exp_date_card(valid_visa_card):
    return {
        **valid_visa_card,
        "exp_date": "99/9999",
    }


@fixture
def invalid_exp_date_expired(valid_visa_card):
    return {
        **valid_visa_card,
        "exp_date": "01/3000",
    }


@fixture
def invalid_holder(valid_visa_card):
    return {
        **valid_visa_card,
        "holder": "?",
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


def test_create_card_endpoint_should_fail_invalid_holder(invalid_holder):
    response = client.post("/card", json=invalid_holder)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert re.match(r".*at least 2 characters.*", response.text)
