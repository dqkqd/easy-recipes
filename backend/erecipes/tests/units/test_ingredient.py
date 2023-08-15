import json

import pytest
from flask.testing import FlaskClient

from erecipes import models, schemas
from erecipes.config import BaseConfig


@pytest.mark.usefixtures("app_context")
def test_200_create_basic(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": "eggs",
            "image": "https://valid-egg-url.com/",
        },
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == {"id": 1}

    ingredient = schemas.Ingredient.model_validate(
        models.Ingredient.query.filter_by(id=1).first_or_404()
    )
    assert ingredient.model_dump(mode="json") == {
        "id": 1,
        "name": "eggs",
        "image": "https://valid-egg-url.com/",
    }


@pytest.mark.usefixtures("app_context")
def test_200_create_duplicated_name(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": "eggs",
            "image": "https://valid-egg1-url.com/",
        },
    )

    # add the same ingredient with different name
    response = client.post(
        "/ingredients/",
        json={
            "name": "eggs",
            "image": "https://valid-egg2-url.com/",
        },
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == {"id": 2}
    ingredient = schemas.Ingredient.model_validate(
        models.Ingredient.query.filter_by(id=2).first_or_404()
    )
    assert ingredient.model_dump(mode="json") == {
        "id": 2,
        "name": "eggs_1",
        "image": "https://valid-egg2-url.com/",
    }


@pytest.mark.usefixtures("app_context")
def test_200_create_use_default_image_url(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": "eggs",
        },
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"id": 1}
    ingredient = schemas.Ingredient.model_validate(
        models.Ingredient.query.filter_by(id=1).first_or_404()
    )
    assert ingredient.model_dump(mode="json") == {
        "id": 1,
        "name": "eggs",
        "image": BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri(),
    }


def test_200_create_uploaded_image_url(client: FlaskClient) -> None:
    raise NotImplementedError("save user uploaded image")


def test_200_create_crop_user_uploaded_image(client: FlaskClient) -> None:
    raise NotImplementedError


@pytest.mark.parametrize(
    ("name", "image", "error_message"),
    [
        # invalid name
        (None, None, "Invalid name."),
        (None, "https://valid-ingredient-url.com", "Invalid name."),
        (None, "https://invalid-ingredient-url", "Invalid name."),
        ("", "https://valid-ingredient-url.com", "Invalid name."),
        (" ", "https://valid-ingredient-url.com", "Invalid name."),
        # invalid url
        ("egg", "https://invalid-ingredient-url", "Invalid image."),
        ("egg", " ", "Invalid image."),
    ],
)
def test_422_create_invalid_name_or_url(
    client: FlaskClient, name: str | None, image: str | None, error_message: str
) -> None:
    payload = {}
    if name is not None:
        payload["name"] = name
    if image is not None:
        payload["image"] = image

    response = client.post("/ingredients/", json=payload)

    data = json.loads(response.data)

    assert response.status_code == 422
    assert data == {"message": error_message}


def test_422_create_invalid_image(client: FlaskClient) -> None:
    raise NotImplementedError("valid url but invalid image")


@pytest.mark.skip()
def test_401_create_unauthorize(client: FlaskClient) -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_403_create_no_permission(client: FlaskClient) -> None:
    raise NotImplementedError
