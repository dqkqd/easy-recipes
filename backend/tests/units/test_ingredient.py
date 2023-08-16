from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from app.config import BaseConfig
from app.models.database import db
from app.models.repositories.ingredient import IngredientRepository
from tests import mock_data

if TYPE_CHECKING:
    from flask.testing import FlaskClient


@pytest.mark.usefixtures("app_context")
def test_200_create_basic(client: FlaskClient) -> None:
    ingredient_data = mock_data.ingredient_create_data()
    response = client.post(
        "/ingredients/",
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    with IngredientRepository.get_repository(db) as repo:
        ingredient = repo.get_ingredient(id=1)
        assert ingredient.model_dump(mode="json") == {
            "id": 1,
            "recipes": [],
            **ingredient_data,
        }


@pytest.mark.usefixtures("app_context")
def test_200_create_use_default_image_url(client: FlaskClient) -> None:
    ingredient_data = mock_data.ingredient_create_data()
    ingredient_data.pop("image")
    response = client.post(
        "/ingredients/",
        json=ingredient_data,
    )
    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    with IngredientRepository.get_repository(db) as repo:
        ingredient = repo.get_ingredient(id=1)
        assert str(ingredient.image) == BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri()


@pytest.mark.usefixtures("app_context")
def test_200_create_name_stripped(client: FlaskClient) -> None:
    ingredient_data = mock_data.ingredient_create_data(name="  eggs  ")
    response = client.post(
        "/ingredients/",
        json=ingredient_data,
    )
    assert response.status_code == 200
    with IngredientRepository.get_repository(db) as repo:
        ingredient = repo.get_ingredient(id=1)
        assert ingredient.name == "eggs"


@pytest.mark.skip("Update after implementing front-end")
def test_200_create_uploaded_image_url(client: FlaskClient) -> None:  # noqa: ARG001
    msg = "save user uploaded image"
    raise NotImplementedError(msg)


@pytest.mark.skip("Update after implementing front-end")
def test_200_create_crop_user_uploaded_image(client: FlaskClient) -> None:  # noqa: ARG001
    raise NotImplementedError


@pytest.mark.parametrize(
    ("name", "image", "error_message"),
    [
        # invalid name
        (None, None, "Invalid name."),
        (None, "https://valid-ingredient-url.com", "Invalid name."),
        (None, "invalid-url.com", "Invalid name."),
        ("", "https://valid-ingredient-url.com", "Invalid name."),
        (" ", "https://valid-ingredient-url.com", "Invalid name."),
        # invalid url
        ("egg", "invalid-url.com", "Invalid image."),
        ("egg", " ", "Invalid image."),
    ],
)
def test_422_create_invalid_name_or_url(
    client: FlaskClient,
    name: str | None,
    image: str | None,
    error_message: str,
) -> None:
    payload = {}
    if name is not None:
        payload["name"] = name
    if image is not None:
        payload["image"] = image

    response = client.post("/ingredients/", json=payload)

    data = json.loads(response.data)

    assert data == {"message": error_message}
    assert response.status_code == 422


@pytest.mark.skip("Update after implementing front-end")
def test_422_create_invalid_image(client: FlaskClient) -> None:  # noqa: ARG001
    msg = "valid url but invalid image"
    raise NotImplementedError(msg)


@pytest.mark.skip("Update after implementing authorization")
def test_401_create_unauthorize(client: FlaskClient) -> None:  # noqa: ARG001
    raise NotImplementedError


@pytest.mark.skip("Update after implementing authorization")
def test_403_create_no_permission(client: FlaskClient) -> None:  # noqa: ARG001
    raise NotImplementedError


def test_200_get_ingredient_basic(client: FlaskClient) -> None:
    ingredient_data = mock_data.ingredient_create_data()
    client.post("/ingredients/", json=ingredient_data)

    response = client.get("/ingredients/1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == {
        "id": 1,
        "recipes": [],
        **ingredient_data,
    }


def test_200_get_ingredient_after_many_posts(client: FlaskClient) -> None:
    num_datas = 5

    ingredient_datas = [mock_data.ingredient_create_data() for _ in range(num_datas)]
    for data in ingredient_datas:
        client.post("/ingredients/", json=data)

    for ingredient_id in range(1, num_datas + 1):
        response = client.get(f"/ingredients/{ingredient_id}")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data["id"] == ingredient_id


def test_404_get_invalid_ingredient(client: FlaskClient) -> None:
    response = client.get("/ingredients/1")
    data = json.loads(response.data)
    assert data == {"message": "Not Found."}
    assert response.status_code == 404
