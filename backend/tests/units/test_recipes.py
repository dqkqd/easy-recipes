from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from pydantic_core import Url

from app import auth, config
from app.crud import crud_recipe
from app.schemas.recipe import Recipe, RecipeUpdate
from tests.mocks import MockAuth, MockRecipe
from tests.utils import compare_image_data_from_uri

if TYPE_CHECKING:
    from flask.testing import FlaskClient


@pytest.mark.usefixtures("app_context")
def test_200_create_basic(client: FlaskClient) -> None:
    recipe_create = MockRecipe.random()
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_create.model_dump(mode="json"),
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    recipe = crud_recipe.get(id=1)

    assert recipe.id == 1
    assert recipe.name == recipe_create.name

    # same image but different url
    assert isinstance(recipe_create.image_uri, Url)
    assert Url(recipe.image_uri) != recipe_create.image_uri
    assert compare_image_data_from_uri(
        Url(recipe.image_uri),
        recipe_create.image_uri,
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
    recipe_data = MockRecipe.random_data()
    recipe_data["name"] = name
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data == {"code": 422, "message": "Invalid name."}


def test_422_create_no_name_provided(client: FlaskClient) -> None:
    recipe_data = MockRecipe.random_data()
    recipe_data.pop("name")
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data == {"code": 422, "message": "Invalid name."}


@pytest.mark.usefixtures("app_context")
def test_200_create_name_stripped(client: FlaskClient) -> None:
    recipe_data = MockRecipe.random_data()
    recipe_data["name"] = "   eggs  "

    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    assert response.status_code == 200

    recipe = crud_recipe.get(id=1)
    assert recipe.name == "eggs"


@pytest.mark.usefixtures("app_context")
def test_200_create_empty_image_uri(client: FlaskClient) -> None:
    recipe_data = MockRecipe.random_data()
    recipe_data["image_uri"] = None
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    recipe = crud_recipe.get(id=1)
    assert recipe.image_uri is None


@pytest.mark.usefixtures("app_context")
def test_200_create_no_image_uri_provided(client: FlaskClient) -> None:
    recipe_data = MockRecipe.random_data()
    recipe_data.pop("image_uri")
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    data = json.loads(response.data)
    assert data == {"id": 1}
    assert response.status_code == 200

    recipe = crud_recipe.get(id=1)
    assert recipe.image_uri is None


@pytest.mark.usefixtures("app_context")
def test_422_create_invalid_uri(client: FlaskClient) -> None:
    recipe_data = MockRecipe.random_data()
    recipe_data["image_uri"] = "invalid"
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data == {"code": 422, "message": "Invalid image_uri."}


@pytest.mark.usefixtures("app_context")
def test_415_create_valid_uri_but_invalid_image(client: FlaskClient) -> None:
    recipe_data = MockRecipe.random_data()
    recipe_data["image_uri"] = "https://example.com"
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_data,
    )

    data = json.loads(response.data)
    assert response.status_code == 415
    assert data == {"code": 415, "message": "Invalid image."}


@pytest.mark.skip("Update after implementing recipes")
def test_200_create_recipe_with_added_recipes() -> None:
    raise NotImplementedError


@pytest.mark.skip("Update after implementing recipes")
def test_422_create_recipe_with_invalid_recipes() -> None:
    raise NotImplementedError


def test_200_get_recipe_basic(client: FlaskClient) -> None:
    recipe_create = MockRecipe.random()
    response = client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_create.model_dump(mode="json"),
    )

    response = client.get("/recipes/1")
    data = json.loads(response.data)
    recipe = Recipe(**data)

    assert response.status_code == 200
    assert recipe_create.model_dump(
        exclude={"image_uri"},
    ) == recipe.model_dump(exclude={"id", "image_uri"})

    assert isinstance(recipe_create.image_uri, Url)
    assert recipe_create.image_uri != recipe.image_uri
    assert compare_image_data_from_uri(
        recipe_create.image_uri,
        recipe.image_uri,
    )


def test_200_get_recipe_after_many_create(client: FlaskClient) -> None:
    num_datas = 5

    for _ in range(num_datas):
        client.post(
            "/recipes/",
            headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
            json=MockRecipe.random_data(),
        )

    for recipe_id in range(1, num_datas + 1):
        response = client.get(f"/recipes/{recipe_id}")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data["id"] == recipe_id


@pytest.mark.skip()
def test_200_get_recipe_with_added_recipes() -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_200_get_recipe_should_give_proper_image() -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_200_get_recipe_unwated_items_are_not_exposed() -> None:
    raise NotImplementedError


def test_404_get_invalid_recipe(client: FlaskClient) -> None:
    response = client.get("/recipes/1")
    data = json.loads(response.data)
    assert data == {"code": 404, "message": "Resources not found."}
    assert response.status_code == 404


def test_200_delete_basic(client: FlaskClient) -> None:
    client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=MockRecipe.random_data(),
    )
    response = client.get("/recipes/1")
    assert response.status_code == 200

    response = client.delete(
        "/recipes/1",
        headers=MockAuth.header(auth.DELETE_RECIPE_PERMISSION),
    )
    assert response.status_code == 200


def test_404_delete_non_existed(client: FlaskClient) -> None:
    response = client.delete(
        "/recipes/1",
        headers=MockAuth.header(auth.DELETE_RECIPE_PERMISSION),
    )
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data == {"code": 404, "message": "Resources not found."}


def test_404_delete_twice(client: FlaskClient) -> None:
    client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=MockRecipe.random_data(),
    )
    response = client.delete(
        "/recipes/1",
        headers=MockAuth.header(auth.DELETE_RECIPE_PERMISSION),
    )
    assert response.status_code == 200

    response = client.delete(
        "/recipes/1",
        headers=MockAuth.header(auth.DELETE_RECIPE_PERMISSION),
    )
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data == {"code": 404, "message": "Resources not found."}


def test_200_get_all(client: FlaskClient) -> None:
    num_datas = 15

    inserted_recipes_data = []
    for _ in range(num_datas):
        data = MockRecipe.random_data()
        client.post(
            "/recipes/",
            headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
            json=data,
        )
        inserted_recipes_data.append(data)

    response = client.get("/recipes/all")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["total"] == num_datas

    for response_data, inserted_data in zip(
        data["recipes"],
        inserted_recipes_data,
    ):
        response_data.pop("image_uri")
        response_data.pop("id")

        inserted_data.pop("image_uri")

        assert response_data == inserted_data


def test_200_get_all_no_data(client: FlaskClient) -> None:
    response = client.get("/recipes/all")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data == {"total": 0, "recipes": []}


def test_200_get_all_after_deletion(client: FlaskClient) -> None:
    num_datas = 15
    num_delete_datas = num_datas // 2

    inserted_recipes_data = []
    for _ in range(num_datas):
        data = MockRecipe.random_data()
        client.post(
            "/recipes/",
            headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
            json=data,
        )
        inserted_recipes_data.append(data)

    response = client.get("/recipes/all")
    assert response.status_code == 200

    for recipe_id in range(1, num_delete_datas + 1):
        response = client.delete(
            f"/recipes/{recipe_id}",
            headers=MockAuth.header(auth.DELETE_RECIPE_PERMISSION),
        )
        assert response.status_code == 200

    response = client.get("/recipes/all")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == num_datas - num_delete_datas


def test_200_get_pagination_basic(client: FlaskClient) -> None:
    total_pages = 2
    last_page_items = config.RECIPES_PAGINATION_SIZE // 2
    num_datas = total_pages * config.RECIPES_PAGINATION_SIZE + last_page_items

    for _ in range(num_datas):
        data = MockRecipe.random_data()
        client.post(
            "/recipes/",
            headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
            json=data,
        )

    for page in range(1, total_pages + 2):
        response = client.get(f"/recipes/?page={page}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total"] == num_datas

        assert data["page"] == page
        if page != total_pages + 1:
            assert len(data["recipes"]) == config.RECIPES_PAGINATION_SIZE
        else:
            assert len(data["recipes"]) == last_page_items


def test_200_get_pagination_no_param(client: FlaskClient) -> None:
    data = MockRecipe.random_data()
    client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=data,
    )

    response = client.get("/recipes/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == 1
    assert data["page"] == 1
    assert len(data["recipes"]) == 1


def test_404_get_page_does_not_exist(client: FlaskClient) -> None:
    data = MockRecipe.random_data()
    client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=data,
    )

    response = client.get("/recipes/100")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data == {"code": 404, "message": "Resources not found."}


def test_404_get_page_no_items(client: FlaskClient) -> None:
    response = client.get("/recipes/")
    data = json.loads(response.data)
    assert data == {
        "page": 1,
        "recipes": [],
        "total": 0,
        "per_page": config.RECIPES_PAGINATION_SIZE,
    }
    assert response.status_code == 200

    response = client.get("/recipes/?page=1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == {
        "page": 1,
        "recipes": [],
        "total": 0,
        "per_page": config.RECIPES_PAGINATION_SIZE,
    }


def test_200_404_pagination_render_enough(client: FlaskClient) -> None:
    for _ in range(config.RECIPES_PAGINATION_SIZE * 2):
        data = MockRecipe.random_data()
        client.post(
            "/recipes/",
            headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
            json=data,
        )

    response = client.get("/recipes/?page=1")
    assert response.status_code == 200

    response = client.get("/recipes/?page=2")
    assert response.status_code == 200

    response = client.get("/recipes/?page=3")
    assert response.status_code == 404


def test_200_recipe_update(client: FlaskClient) -> None:
    recipe_create = MockRecipe.random()
    client.post(
        "/recipes/",
        headers=MockAuth.header(auth.CREATE_RECIPE_PERMISSION),
        json=recipe_create.model_dump(mode="json"),
    )

    recipe_update = RecipeUpdate(**MockRecipe.random_data())
    response = client.patch(
        "/recipes/1",
        headers=MockAuth.header(auth.UPDATE_RECIPE_PERMISSION),
        json=recipe_update.model_dump(mode="json"),
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data.pop("id") == 1
    assert isinstance(recipe_update.image_uri, Url)
    compare_image_data_from_uri(recipe_update.image_uri, Url(data.pop("image_uri")))
    assert data == recipe_update.model_dump(mode="json", exclude={"image_uri"})
