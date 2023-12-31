from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from pydantic_core import Url

from app import auth, config
from app.crud import crud_ingredient
from app.schemas.ingredient import Ingredient, IngredientUpdate
from tests.mocks import MockAuth, MockIngredient
from tests.utils import compare_image_data_from_uri

if TYPE_CHECKING:
    from flask.testing import FlaskClient


@pytest.mark.usefixtures("app_context")
def test_200_create_basic(client: FlaskClient) -> None:
    ingredient_create = MockIngredient.random()
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_create.model_dump(mode="json"),
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    ingredient = crud_ingredient.get(id=1)

    assert ingredient.id == 1
    assert ingredient.name == ingredient_create.name
    assert ingredient.likes == 0

    # same image but different url
    assert isinstance(ingredient_create.image_uri, Url)
    assert Url(ingredient.image_uri) != ingredient_create.image_uri
    assert compare_image_data_from_uri(
        Url(ingredient.image_uri),
        ingredient_create.image_uri,
    )


@pytest.mark.parametrize(
    "name",
    [
        None,
        "",
        " ",
    ],
)
def test_422_create_invalid_name(client: FlaskClient, name: str | None) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data["name"] = name
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data == {"code": 422, "message": "Invalid name."}


def test_422_create_no_name_provided(client: FlaskClient) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data.pop("name")
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data == {"code": 422, "message": "Invalid name."}


@pytest.mark.usefixtures("app_context")
def test_200_create_name_stripped(client: FlaskClient) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data["name"] = "   eggs  "

    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    assert response.status_code == 200

    ingredient = crud_ingredient.get(id=1)
    assert ingredient.name == "eggs"


@pytest.mark.usefixtures("app_context")
def test_200_create_empty_image_uri(client: FlaskClient) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data["image_uri"] = None
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    ingredient = crud_ingredient.get(id=1)
    assert ingredient.image_uri is None


@pytest.mark.usefixtures("app_context")
def test_200_create_no_image_uri_provided(client: FlaskClient) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data.pop("image_uri")
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    ingredient = crud_ingredient.get(id=1)
    assert ingredient.image_uri is None


@pytest.mark.usefixtures("app_context")
def test_422_create_invalid_uri(client: FlaskClient) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data["image_uri"] = "invalid"
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data == {"code": 422, "message": "Invalid image_uri."}


@pytest.mark.usefixtures("app_context")
def test_415_create_valid_uri_but_invalid_image(client: FlaskClient) -> None:
    ingredient_data = MockIngredient.random_data()
    ingredient_data["image_uri"] = "https://example.com"
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 415
    assert data == {"code": 415, "message": "Invalid image."}


@pytest.mark.skip("Update after implementing recipes")
def test_200_create_ingredient_with_added_recipes() -> None:
    raise NotImplementedError


@pytest.mark.skip("Update after implementing recipes")
def test_422_create_ingredient_with_invalid_recipes() -> None:
    raise NotImplementedError


def test_200_get_ingredient_basic(client: FlaskClient) -> None:
    ingredient_create = MockIngredient.random()
    response = client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_create.model_dump(mode="json"),
    )

    response = client.get("/ingredients/1")
    data = json.loads(response.data)
    ingredient = Ingredient(**data)

    assert response.status_code == 200

    assert (
        ingredient_create.model_dump(exclude={"image_uri"}).items()
        <= ingredient.model_dump().items()
    )

    assert isinstance(ingredient_create.image_uri, Url)
    assert ingredient_create.image_uri != ingredient.image_uri
    assert compare_image_data_from_uri(
        ingredient_create.image_uri,
        ingredient.image_uri,
    )


def test_200_get_ingredient_after_many_create(client: FlaskClient) -> None:
    num_datas = 5

    for _ in range(num_datas):
        client.post(
            "/ingredients/",
            headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
            json=MockIngredient.random_data(),
        )

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
    assert data == {"code": 404, "message": "Resources not found."}
    assert response.status_code == 404


def test_200_delete_basic(client: FlaskClient) -> None:
    client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_data(),
    )
    response = client.get("/ingredients/1")
    assert response.status_code == 200

    response = client.delete(
        "/ingredients/1",
        headers=MockAuth.header(auth.DELETE_INGREDIENT_PERMISSION),
    )
    assert response.status_code == 200


def test_404_delete_non_existed(client: FlaskClient) -> None:
    response = client.delete(
        "/ingredients/1",
        headers=MockAuth.header(auth.DELETE_INGREDIENT_PERMISSION),
    )
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data == {"code": 404, "message": "Resources not found."}


def test_404_delete_twice(client: FlaskClient) -> None:
    client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_data(),
    )
    response = client.delete(
        "/ingredients/1",
        headers=MockAuth.header(auth.DELETE_INGREDIENT_PERMISSION),
    )
    assert response.status_code == 200

    response = client.delete(
        "/ingredients/1",
        headers=MockAuth.header(auth.DELETE_INGREDIENT_PERMISSION),
    )
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data == {"code": 404, "message": "Resources not found."}


def test_200_get_all(client: FlaskClient) -> None:
    num_datas = 15

    inserted_ingredients_data = []
    for _ in range(num_datas):
        data = MockIngredient.random_data()
        client.post(
            "/ingredients/",
            headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
            json=data,
        )
        inserted_ingredients_data.append(data)

    response = client.get("/ingredients/all")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["total"] == num_datas

    for response_data, inserted_data in zip(
        data["ingredients"],
        inserted_ingredients_data,
    ):
        response_data.pop("image_uri")
        response_data.pop("id")

        inserted_data.pop("image_uri")

        assert response_data.items() >= inserted_data.items()


def test_200_get_all_no_data(client: FlaskClient) -> None:
    response = client.get("/ingredients/all")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data == {"total": 0, "ingredients": []}


def test_200_get_all_after_deletion(client: FlaskClient) -> None:
    num_datas = 15
    num_delete_datas = num_datas // 2

    inserted_ingredients_data = []
    for _ in range(num_datas):
        data = MockIngredient.random_data()
        client.post(
            "/ingredients/",
            headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
            json=data,
        )
        inserted_ingredients_data.append(data)

    response = client.get("/ingredients/all")
    assert response.status_code == 200

    for ingredient_id in range(1, num_delete_datas + 1):
        response = client.delete(
            f"/ingredients/{ingredient_id}",
            headers=MockAuth.header(auth.DELETE_INGREDIENT_PERMISSION),
        )
        assert response.status_code == 200

    response = client.get("/ingredients/all")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == num_datas - num_delete_datas


def test_200_get_pagination_basic(client: FlaskClient) -> None:
    total_pages = 2
    last_page_items = config.INGREDIENTS_PAGINATION_SIZE // 2
    num_datas = total_pages * config.INGREDIENTS_PAGINATION_SIZE + last_page_items

    for _ in range(num_datas):
        data = MockIngredient.random_data()
        client.post(
            "/ingredients/",
            headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
            json=data,
        )

    for page in range(1, total_pages + 2):
        response = client.get(f"/ingredients/?page={page}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total"] == num_datas

        assert data["page"] == page
        if page != total_pages + 1:
            assert len(data["ingredients"]) == config.INGREDIENTS_PAGINATION_SIZE
        else:
            assert len(data["ingredients"]) == last_page_items


def test_200_get_pagination_no_param(client: FlaskClient) -> None:
    data = MockIngredient.random_data()
    client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=data,
    )

    response = client.get("/ingredients/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == 1
    assert data["page"] == 1
    assert len(data["ingredients"]) == 1


def test_200_get_pagination_with_per_page(client: FlaskClient) -> None:
    num_datas = 14
    for _ in range(num_datas):
        client.post(
            "/ingredients/",
            headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
            json=MockIngredient.random_data(),
        )

    response = client.get("/ingredients/?page=2&&per_page=5")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == 14
    assert data["page"] == 2
    assert data["per_page"] == 5
    assert len(data["ingredients"]) == 5


def test_404_get_page_does_not_exist(client: FlaskClient) -> None:
    data = MockIngredient.random_data()
    client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=data,
    )

    response = client.get("/ingredients/100")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data == {"code": 404, "message": "Resources not found."}


def test_404_get_page_no_items(client: FlaskClient) -> None:
    response = client.get("/ingredients/")
    data = json.loads(response.data)
    assert data == {
        "page": 1,
        "ingredients": [],
        "total": 0,
        "per_page": config.INGREDIENTS_PAGINATION_SIZE,
    }
    assert response.status_code == 200

    response = client.get("/ingredients/?page=1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == {
        "page": 1,
        "ingredients": [],
        "total": 0,
        "per_page": config.INGREDIENTS_PAGINATION_SIZE,
    }


def test_200_404_pagination_render_enough(client: FlaskClient) -> None:
    for _ in range(config.INGREDIENTS_PAGINATION_SIZE * 2):
        data = MockIngredient.random_data()
        client.post(
            "/ingredients/",
            headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
            json=data,
        )

    response = client.get("/ingredients/?page=1")
    assert response.status_code == 200

    response = client.get("/ingredients/?page=2")
    assert response.status_code == 200

    response = client.get("/ingredients/?page=3")
    assert response.status_code == 404


def test_200_ingredient_update(client: FlaskClient) -> None:
    ingredient_create = MockIngredient.random()
    client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=ingredient_create.model_dump(mode="json"),
    )

    ingredient_update = IngredientUpdate(**MockIngredient.random_data())
    response = client.patch(
        "/ingredients/1",
        headers=MockAuth.header(auth.UPDATE_INGREDIENT_PERMISSION),
        json=ingredient_update.model_dump(mode="json"),
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data.pop("id") == 1
    assert isinstance(ingredient_update.image_uri, Url)
    compare_image_data_from_uri(ingredient_update.image_uri, Url(data.pop("image_uri")))

    assert (
        data.items()
        >= ingredient_update.model_dump(mode="json", exclude={"image_uri"}).items()
    )


def test_200_like_recipe(client: FlaskClient) -> None:
    client.post(
        "/ingredients/",
        headers=MockAuth.header(auth.CREATE_INGREDIENT_PERMISSION),
        json=MockIngredient.random_data(),
    )

    response = client.get("/ingredients/1")
    data = json.loads(response.data)
    ingredient = Ingredient(**data)

    assert ingredient.likes == 0

    total_likes = 0
    for _ in range(10):
        response = client.post("/ingredients/1/like")
        assert response.status_code == 200
        data = json.loads(response.data)

        total_likes += 1
        assert data == {"id": 1, "total_likes": total_likes}

        response = client.get("/ingredients/1")
        data = json.loads(response.data)
        ingredient = Ingredient(**data)
        assert ingredient.likes == total_likes
