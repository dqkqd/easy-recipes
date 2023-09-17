from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from flask import Blueprint, abort, jsonify, request

from app import auth, config
from app.crud import crud_ingredient, crud_recipe
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.schemas.ingredient import (
    AllIngredients,
    Ingredient,
    IngredientIds,
    PaginatedIngredients,
)
from app.schemas.recipe import (
    AllRecipes,
    PaginatedRecipes,
    Recipe,
    RecipeCreate,
    RecipeUpdate,
)

if TYPE_CHECKING:
    from werkzeug import Response

api = Blueprint("recipes", __name__, url_prefix="/recipes")


@api.route("/all")
@to_handleable_error
def get_recipes() -> Response:
    recipes = crud_recipe.get_all()
    return jsonify(
        AllRecipes(
            total=len(recipes),
            recipes=[Recipe.model_validate(recipe) for recipe in recipes],
        ).model_dump(
            mode="json",
        ),
    )


@api.route("/")
@to_handleable_error
def get_paginations() -> Response:
    pagination_size = config.INGREDIENTS_PAGINATION_SIZE
    with contextlib.suppress(ValueError):
        pagination_size = request.args.get(
            "per_page",
            default=config.RECIPES_PAGINATION_SIZE,
            type=int,
        )

    paginaged_recipes = crud_recipe.get_pagination(pagination_size=pagination_size)

    if paginaged_recipes.page != 1 and paginaged_recipes.page > paginaged_recipes.pages:
        abort(404)

    return jsonify(
        PaginatedRecipes(
            page=paginaged_recipes.page,
            recipes=[Recipe.model_validate(recipe) for recipe in paginaged_recipes],
            total=paginaged_recipes.total or 0,
            per_page=paginaged_recipes.per_page,
        ).model_dump(mode="json"),
    )


@api.route("/<int:id>")
@to_handleable_error
def get_recipe(id: int) -> Response:  # noqa: A002
    return jsonify(
        Recipe.model_validate(crud_recipe.get(id)).model_dump(mode="json"),
    )


@api.route("/", methods=["POST"])
@to_handleable_error
@auth.require(auth.CREATE_RECIPE_PERMISSION)
def create_recipe() -> Response:
    body = request.get_json()

    recipe_create = RecipeCreate(**body)

    if recipe_create.image_uri is not None:
        with ImageOnServer.from_source(recipe_create.image_uri) as image_on_server:
            recipe_create.image_uri = image_on_server.uri

    recipe = crud_recipe.add(recipe_create)
    return jsonify({"id": recipe.id})


@api.route("/<int:id>", methods=["DELETE"])
@to_handleable_error
@auth.require(auth.DELETE_RECIPE_PERMISSION)
def delete_recipe(id: int) -> Response:  # noqa: A002
    crud_recipe.delete(id)
    return jsonify({"id": id})


@api.route("/<int:id>", methods=["PATCH"])
@to_handleable_error
@auth.require(auth.UPDATE_RECIPE_PERMISSION)
def update_recipe(id: int) -> Response:  # noqa: A002
    body = request.get_json()
    recipe_update = RecipeUpdate(**body)

    if recipe_update.image_uri is not None:
        with ImageOnServer.from_source(recipe_update.image_uri) as image_on_server:
            recipe_update.image_uri = image_on_server.uri

    recipe_db = crud_recipe.get(id=id)
    recipe = crud_recipe.update(recipe_db, recipe_update)
    return jsonify(Recipe.model_validate(recipe).model_dump(mode="json"))


@api.route("/<int:id>/like", methods=["POST"])
@to_handleable_error
def like_recipe(id: int) -> Response:  # noqa: A002
    recipe_db = crud_recipe.like(id)
    return jsonify({"id": id, "total_likes": recipe_db.likes})


@api.route("/<int:id>/ingredients/all", methods=["GET"])
@to_handleable_error
def get_ingredients(id: int) -> Response:  # noqa: A002
    recipe = crud_recipe.get(id=id)
    return jsonify(
        AllIngredients(
            total=len(recipe.ingredients),
            ingredients=[
                Ingredient.model_validate(ingredient) for ingredient in recipe.ingredients
            ],
        ).model_dump(mode="json"),
    )


@api.route("/<int:id>/ingredients/", methods=["GET"])
@to_handleable_error
def get_paginated_ingredients(id: int) -> Response:  # noqa: A002
    pagination_size = config.INGREDIENTS_PAGINATION_SIZE
    with contextlib.suppress(ValueError):
        pagination_size = request.args.get(
            "per_page",
            default=config.INGREDIENTS_PAGINATION_SIZE,
            type=int,
        )

    ingredients = crud_ingredient.get_pagination_by_recipe_id(
        recipe_id=id,
        pagination_size=pagination_size,
    )

    return jsonify(
        PaginatedIngredients(
            page=ingredients.page,
            ingredients=[
                Ingredient.model_validate(ingredient) for ingredient in ingredients
            ],
            total=ingredients.total or 0,
            per_page=ingredients.per_page,
        ).model_dump(mode="json"),
    )


@api.route("/<int:id>/ingredients/", methods=["POST"])
@to_handleable_error
@auth.require(auth.UPDATE_RECIPE_PERMISSION)
def add_ingredients(id: int) -> Response:  # noqa: A002
    body = request.get_json()
    ingredient_ids = IngredientIds(**body).ids
    ingredients = [
        crud_ingredient.get(id=ingredient_id) for ingredient_id in ingredient_ids
    ]
    recipe = crud_recipe.add_ingredients(id, ingredients=ingredients)

    return jsonify(Recipe.model_validate(recipe).model_dump(mode="json"))


@api.route("/<int:id>/ingredients/<int:ingredient_id>", methods=["DELETE"])
@to_handleable_error
@auth.require(auth.UPDATE_RECIPE_PERMISSION)
def delete_ingredient(id: int, ingredient_id: int) -> Response:  # noqa: A002
    ingredient = crud_ingredient.get(id=ingredient_id)
    recipe = crud_recipe.delete_ingredient(id, ingredient=ingredient)
    return jsonify(Recipe.model_validate(recipe).model_dump(mode="json"))
