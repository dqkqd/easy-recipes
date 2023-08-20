from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from app import auth
from tests.mocks import MockAuth, MockIngredient

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from pytest_mock import MockerFixture


def test_200_create_ingredient_basic(mocker: MockerFixture, client: FlaskClient) -> None:
    token = auth.CREATE_INGREDIENT_PERMISSION

    mocker.patch(
        "app.auth.verify_decode_jwt",
        return_value={"permissions": [token]},
    )
    response = client.post(
        "/ingredients/",
        headers=MockAuth.authorization_header(token),
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 200


def test_401_create_ingredient_missing_authorization(
    client: FlaskClient,
) -> None:
    response = client.post(
        "/ingredients/",
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 401


@pytest.mark.parametrize(
    "headers",
    [
        None,
        {"Authorization": ""},
        {"Authorization": "Bearer"},
        {"Authorization": "Bearer token with space"},
    ],
)
def test_401_create_ingredient_authorization_invalid(
    headers: dict[str, str],
    client: FlaskClient,
) -> None:
    response = client.post(
        "/ingredients/",
        headers=headers,
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 401
