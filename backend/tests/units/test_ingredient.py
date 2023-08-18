from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

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


@pytest.mark.skip()
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


@pytest.mark.skip()
def test_200_create_ingredient_with_added_recipes() -> None:
    raise NotImplementedError


@pytest.mark.parametrize(
    "name",
    [
        None,
        "",
        " ",
    ],
)
def test_422_create_invalid_name(client: FlaskClient, name: str | None) -> None:
    ingredient_data = mock_data.ingredient_create_data()
    ingredient_data["name"] = name
    response = client.post("/ingredients/", json=ingredient_data)

    data = json.loads(response.data)
    assert data == {"message": "Invalid name."}
    assert response.status_code == 422


@pytest.mark.parametrize(
    "image",
    [
        "this is not a url",
    ],
)
def test_422_create_invalid_url(
    client: FlaskClient,
    image: str | None,
) -> None:
    ingredient_data = mock_data.ingredient_create_data()
    ingredient_data["image"] = image
    response = client.post("/ingredients/", json=ingredient_data)

    data = json.loads(response.data)

    assert data == {"message": "Invalid image."}
    assert response.status_code == 422


@pytest.mark.skip("Update after implementing front-end")
def test_422_create_invalid_image(client: FlaskClient) -> None:  # noqa: ARG001
    msg = "valid url but invalid image"
    raise NotImplementedError(msg)


@pytest.mark.skip()
def test_422_create_ingredient_with_invalid_recipes() -> None:
    raise NotImplementedError


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


@pytest.mark.skip()
def test_200_get_ingredient_with_added_recipes() -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_200_get_ingredient_should_give_proper_image() -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_200_get_ingredient_unwated_items_are_not_exposed() -> None:
    raise NotImplementedError


def test_404_get_invalid_ingredient(client: FlaskClient) -> None:
    response = client.get("/ingredients/1")
    data = json.loads(response.data)
    assert data == {"message": "Not Found."}
    assert response.status_code == 404
