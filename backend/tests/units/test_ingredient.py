import json

import pytest
from flask.testing import FlaskClient

from app.config import BaseConfig
from app.models.database import orm
from app.models.schemas import schema


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
    assert data == {"id": 1}
    assert response.status_code == 200

    ingredient = schema.IngredientInDB.model_validate(
        orm.Ingredient.query.filter_by(id=1).first_or_404()
    )
    assert ingredient.model_dump(mode="json") == {
        "id": 1,
        "name": "eggs",
        "image": "https://valid-egg-url.com/",
        "recipes": [],
    }


@pytest.mark.usefixtures("app_context")
def test_200_create_use_default_image_url(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": "eggs",
        },
    )
    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    ingredient = schema.IngredientInDB.model_validate(
        orm.Ingredient.query.filter_by(id=1).first_or_404()
    )
    assert ingredient.model_dump(mode="json") == {
        "id": 1,
        "name": "eggs",
        "image": BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri(),
        "recipes": [],
    }


@pytest.mark.usefixtures("app_context")
def test_200_create_name_stripped(client: FlaskClient) -> None:
    response = client.post(
        "/ingredients/",
        json={
            "name": " eggs ",
        },
    )
    assert response.status_code == 200
    ingredient = schema.IngredientInDB.model_validate(
        orm.Ingredient.query.filter_by(id=1).first_or_404()
    )
    assert ingredient.model_dump(mode="json") == {
        "id": 1,
        "name": "eggs",
        "image": BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri(),
        "recipes": [],
    }


@pytest.mark.skip("Update after implementing front-end")
def test_200_create_uploaded_image_url(client: FlaskClient) -> None:
    raise NotImplementedError("save user uploaded image")


@pytest.mark.skip("Update after implementing front-end")
def test_200_create_crop_user_uploaded_image(client: FlaskClient) -> None:
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
    client: FlaskClient, name: str | None, image: str | None, error_message: str
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
def test_422_create_invalid_image(client: FlaskClient) -> None:
    raise NotImplementedError("valid url but invalid image")


@pytest.mark.skip("Update after implementing authorization")
def test_401_create_unauthorize(client: FlaskClient) -> None:
    raise NotImplementedError


@pytest.mark.skip("Update after implementing authorization")
def test_403_create_no_permission(client: FlaskClient) -> None:
    raise NotImplementedError
