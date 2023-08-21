from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from app import auth
from tests.mocks import MockAuth, MockIngredient, MockRecipe

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from pytest_mock import MockerFixture


def test_200_create_ingredient_basic(mocker: MockerFixture, client: FlaskClient) -> None:
    token = auth.CREATE_INGREDIENT_PERMISSION

    mocker.patch(
        "app.auth.verify_decode_jwt",
        return_value=auth.Permissions(permissions=[token]),
    )
    response = client.post(
        "/ingredients/",
        headers=MockAuth.authorization_header(token),
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 200


def test_200_create_recipes_basic(mocker: MockerFixture, client: FlaskClient) -> None:
    token = auth.CREATE_RECIPE_PERMISSION

    mocker.patch(
        "app.auth.verify_decode_jwt",
        return_value=auth.Permissions(permissions=[token]),
    )
    response = client.post(
        "/recipes/",
        headers=MockAuth.authorization_header(token),
        json=MockRecipe.random_valid_recipe_data(),
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
    data = json.loads(response.data)
    assert data == {"code": 401, "message": "Unauthorized."}

    response = client.post(
        "/recipes/",
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data == {"code": 401, "message": "Unauthorized."}


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": ""},
        {"Authorization": "Bearer"},
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
    data = json.loads(response.data)
    assert data == {"code": 401, "message": "Unauthorized."}

    response = client.post(
        "/recipes/",
        headers=headers,
        json=MockRecipe.random_valid_recipe_data(),
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data == {"code": 401, "message": "Unauthorized."}
