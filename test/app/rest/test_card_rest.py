from datetime import datetime
from unittest.mock import patch, MagicMock

import bcrypt
import pytest
from bson import ObjectId
from fastapi.testclient import TestClient
from httpx import Response
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

fake_user = dict(username="admin", password="admin")


@pytest.fixture
def auth_headers():
    response = client.post("/users", json=fake_user)
    assert response.status_code == status.HTTP_201_CREATED, response.text

    response = client.post("/token", data=fake_user)
    assert response.status_code == status.HTTP_200_OK, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def make_encrypt_faster():
    def quicker_encrypt(s: str):
        encrypted = bcrypt.hashpw(s.encode(), bcrypt.gensalt(rounds=4))
        return encrypted.decode()

    with (
        patch("app.business.user.encrypt") as encrypt_pwd,
        patch("app.domain.card.encrypt") as encrypt_card
    ):
        encrypt_pwd.side_effect = quicker_encrypt
        encrypt_card.side_effect = quicker_encrypt
        yield


@pytest.mark.parametrize("response", [
    client.get("/cards"),
    client.get("/cards/123"),
    client.post("/cards"),
])
def test_should_fail_unauthorized_missing_headers(response: Response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


@pytest.mark.parametrize("response", [
    client.get("/cards", headers={"Authorization": "Bearer invalid_token"}),
    client.get("/cards/123", headers={"Authorization": "Bearer invalid_token"}),
    client.post("/cards", headers={"Authorization": "Bearer invalid_token"}),
])
def test_should_fail_unauthorized_invalid_credentials(response: Response):
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_should_fail_attempt_to_login_with_nonexistent_user():
    user = dict(username="no-one", password="irrelevant")
    response = client.post("/token", data=user)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_should_fail_attempt_to_login_with_invalid_password():
    user = dict(username="admin", password="admin")
    assert client.post("/users", json=user).status_code == status.HTTP_201_CREATED

    response = client.post("/token", data=dict(username="admin", password="wrong"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_create_card_endpoint_should_fail_exp_date(auth_headers):
    invalid_exp_date_card = {**valid_visa_card, "exp_date": "99/9999"}
    response = client.post("/cards", json=invalid_exp_date_card, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "is not a valid date" in response.text


@patch("app.business.validators.utcnow")
def test_create_card_endpoint_should_fail_expired(mock_utcnow: MagicMock, auth_headers):
    invalid_exp_date_expired = {**valid_visa_card, "exp_date": "01/3000"}
    mock_utcnow.return_value = as_utc(datetime.fromisoformat("4000-01-01"))
    response = client.post("/cards", json=invalid_exp_date_expired, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "already expired" in response.text


def test_create_card_endpoint_should_fail_invalid_holder(auth_headers):
    invalid_holder = {**valid_visa_card, "holder": "?"}
    response = client.post("/cards", json=invalid_holder, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "at least 2 characters" in response.text


def test_create_card_endpoint_should_fail_invalid_cvv_low(auth_headers):
    invalid_cvv = {**valid_visa_card, "cvv": "10"}
    response = client.post("/cards", json=invalid_cvv, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "greater than or equal to 100" in response.text


def test_create_card_endpoint_should_fail_invalid_cvv_high(auth_headers):
    invalid_cvv = {**valid_visa_card, "cvv": "99999"}
    response = client.post("/cards", json=invalid_cvv, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "less than or equal to 9999" in response.text


def test_create_card_endpoint_should_fail_invalid_number_format(auth_headers):
    invalid_number = {**valid_visa_card, "number": "not a number"}
    response = client.post("/cards", json=invalid_number, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "should match pattern" in response.text


def test_create_card_endpoint_should_fail_invalid_number(auth_headers):
    invalid_number = {**valid_visa_card, "number": "123456"}
    response = client.post("/cards", json=invalid_number, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
    assert "Invalid credit card number" in response.text


def test_card_is_stored_in_database(auth_headers):
    create_response = client.post("/cards", json=valid_visa_card, headers=auth_headers)
    assert create_response.status_code == status.HTTP_201_CREATED, create_response.text
    created_card = create_response.json()
    assert created_card["created_by"] == fake_user["username"]

    ignore = frozenset({"number", "created_at"})

    _cmp_dict(valid_visa_card, created_card, ignore=ignore)

    find_response = client.get(f"/cards/{created_card['id']}", headers=auth_headers)
    assert find_response.status_code == status.HTTP_200_OK, find_response.text
    found_card = find_response.json()

    _cmp_dict(created_card, found_card, ignore=ignore)


def test_should_not_find_card(auth_headers):
    nonexistent_id = str(ObjectId())
    find_response = client.get(f"/cards/{nonexistent_id}", headers=auth_headers)
    assert find_response.status_code == status.HTTP_404_NOT_FOUND, find_response.text


@pytest.mark.slow
def test_should_find_all_cards(auth_headers):
    _populate_database(10, auth_headers)

    response = client.get("/cards", params={"skip": 0, "limit": 8}, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert len(response.json()) == 8

    response = client.get("/cards", params={"skip": 8, "limit": 100}, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert len(response.json()) == 2

    response = client.get("/cards", params={"skip": 10, "limit": 100}, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert len(response.json()) == 0


def test_should_fail_to_create_duplicated_cards(auth_headers):
    response = client.post("/cards", json=valid_visa_card, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED, response.text

    response = client.post("/cards", json=valid_visa_card, headers=auth_headers)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text

    assert "already exists" in response.text


def _populate_database(n: int, auth_headers: dict):
    for i in range(n):
        holder = f"CLIENT-{i}"
        response = client.post("/cards", json={**valid_visa_card, "holder": holder}, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED


def _cmp_dict(d1: dict, d2: dict, *, ignore=frozenset[str]()):
    cleaned_d1 = {k: v for k, v in d1.items() if k not in ignore}
    cleaned_d2 = {k: v for k, v in d2.items() if k not in ignore}

    assert cleaned_d1.items() <= cleaned_d2.items()
