from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from app import auth
from tests.mocks import MockAuth, MockIngredient, MockRecipe

if TYPE_CHECKING:
    from flask.testing import FlaskClient


def test_200_create_ingredient(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        headers=MockAuth.authorization_header(auth.CREATE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 200


def test_200_delete_ingredient(client: FlaskClient) -> None:
    client.post(
        "/ingredients/",
        headers=MockAuth.authorization_header(auth.CREATE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_valid_ingredient_data(),
    )

    response = client.delete(
        "/ingredients/1",
        headers=MockAuth.authorization_header(auth.DELETE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_valid_ingredient_data(),
    )
    assert response.status_code == 200


def test_200_create_recipe(client: FlaskClient) -> None:
    response = client.post(
        "/recipes/",
        headers=MockAuth.authorization_header(auth.CREATE_RECIPE_PERMISSION),
        json=MockRecipe.random_valid_recipe_data(),
    )
    assert response.status_code == 200


def test_200_delete_recipe(client: FlaskClient) -> None:
    client.post(
        "/recipes/",
        headers=MockAuth.authorization_header(auth.CREATE_RECIPE_PERMISSION),
        json=MockRecipe.random_valid_recipe_data(),
    )

    response = client.delete(
        "/recipes/1",
        headers=MockAuth.authorization_header(auth.DELETE_RECIPE_PERMISSION),
        json=MockRecipe.random_valid_recipe_data(),
    )
    assert response.status_code == 200


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


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": ""},
        {"Authorization": "Bearer"},
    ],
)
def test_401_delete_ingredient_authorization_invalid(
    headers: dict[str, str],
    client: FlaskClient,
) -> None:
    response = client.post(
        "/ingredients/",
        headers=MockAuth.authorization_header(auth.CREATE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_valid_ingredient_data(),
    )

    response = client.delete(
        "/ingredients/1",
        headers=headers,
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
def test_401_create_recipe_authorization_invalid(
    headers: dict[str, str],
    client: FlaskClient,
) -> None:
    response = client.post(
        "/recipes/",
        headers=headers,
        json=MockRecipe.random_valid_recipe_data(),
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
def test_401_delete_recipe_authorization_invalid(
    headers: dict[str, str],
    client: FlaskClient,
) -> None:
    response = client.post(
        "/recipes/",
        headers=MockAuth.authorization_header(auth.CREATE_RECIPE_PERMISSION),
        json=MockRecipe.random_valid_recipe_data(),
    )

    response = client.delete(
        "/recipes/1",
        headers=headers,
        json=MockRecipe.random_valid_recipe_data(),
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data == {"code": 401, "message": "Unauthorized."}
