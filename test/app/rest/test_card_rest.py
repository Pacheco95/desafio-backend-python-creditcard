from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from starlette import status

from app.main import app
from app.utils.datetime import as_utc

client = TestClient(app)

valid_visa_card = {
    "exp_date": "10/2025",
    "holder": "FULANO DA SILVA",
    "number": "4220036484096326",
    "cvv": 606,
}


def _cmp_dict(d1: dict, d2: dict, *, ignore=frozenset[str]()):
    cleaned_d1 = {k: v for k, v in d1.items() if k not in ignore}
    cleaned_d2 = {k: v for k, v in d2.items() if k not in ignore}

    assert cleaned_d1.items() <= cleaned_d2.items()


def test_create_card_endpoint_should_fail_exp_date():
    invalid_exp_date_card = {**valid_visa_card, "exp_date": "99/9999"}
    response = client.post("/card", json=invalid_exp_date_card)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "is not a valid date" in response.text


@patch("app.business.validators.utcnow")
def test_create_card_endpoint_should_fail_expired(mock_utcnow: MagicMock):
    invalid_exp_date_expired = {**valid_visa_card, "exp_date": "01/3000"}
    mock_utcnow.return_value = as_utc(datetime.fromisoformat("4000-01-01"))
    response = client.post("/card", json=invalid_exp_date_expired)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "already expired" in response.text


def test_create_card_endpoint_should_fail_invalid_holder():
    invalid_holder = {**valid_visa_card, "holder": "?"}
    response = client.post("/card", json=invalid_holder)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "at least 2 characters" in response.text


def test_create_card_endpoint_should_fail_invalid_cvv_low():
    invalid_cvv = {**valid_visa_card, "cvv": "10"}
    response = client.post("/card", json=invalid_cvv)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "greater than or equal to 100" in response.text


def test_create_card_endpoint_should_fail_invalid_cvv_high():
    invalid_cvv = {**valid_visa_card, "cvv": "99999"}
    response = client.post("/card", json=invalid_cvv)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "less than or equal to 9999" in response.text


def test_create_card_endpoint_should_fail_invalid_number_format():
    invalid_number = {**valid_visa_card, "number": "not a number"}
    response = client.post("/card", json=invalid_number)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "should match pattern" in response.text


def test_create_card_endpoint_should_fail_invalid_number():
    invalid_number = {**valid_visa_card, "number": "123456"}
    response = client.post("/card", json=invalid_number)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "Invalid credit card number" in response.text


def test_create_card_endpoint_should_succeed():
    create_response = client.post("/card", json=valid_visa_card)
    assert create_response.status_code == status.HTTP_201_CREATED, create_response.text
    created_card = create_response.json()

    _cmp_dict(valid_visa_card, created_card, ignore=frozenset({"number"}))

    find_response = client.get(f"/card/{created_card['id']}")
    assert find_response.status_code == status.HTTP_200_OK, find_response.text
    found_card = find_response.json()

    _cmp_dict(created_card, found_card, ignore=frozenset({"number"}))


def test_should_not_find_card():
    nonexistent_id = str(ObjectId())
    find_response = client.get(f"/card/{nonexistent_id}")
    assert find_response.status_code == status.HTTP_404_NOT_FOUND, find_response.text


@pytest.mark.slow
def test_should_find_all_cards():
    _populate_database(10)

    response = client.get("card", params={"skip": 0, "limit": 8})
    assert response.status_code == status.HTTP_200_OK, response.text
    assert len(response.json()) == 8

    response = client.get("card", params={"skip": 8, "limit": 100})
    assert response.status_code == status.HTTP_200_OK, response.text
    assert len(response.json()) == 2

    response = client.get("card", params={"skip": 10, "limit": 100})
    assert response.status_code == status.HTTP_200_OK, response.text
    assert len(response.json()) == 0


def test_should_fail_to_create_duplicated_cards():
    response = client.post("/card", json=valid_visa_card)
    assert response.status_code == status.HTTP_201_CREATED, response.text

    response = client.post("/card", json=valid_visa_card)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text

    assert "already exists" in response.text


def _populate_database(n: int):
    for i in range(n):
        holder = f"CLIENT-{i}"
        response = client.post("/card", json={**valid_visa_card, "holder": holder})
        assert response.status_code == status.HTTP_201_CREATED
