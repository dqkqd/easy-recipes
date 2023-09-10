from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, abort, jsonify, request

from app import auth, config
from app.crud import crud_recipe
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate

if TYPE_CHECKING:
    from werkzeug import Response

api = Blueprint("recipes", __name__, url_prefix="/recipes")


@api.route("/all")
@to_handleable_error
def get_recipes() -> Response:
    recipes = crud_recipe.get_all()
    return jsonify(
        {
            "total": len(recipes),
            "recipes": [
                Recipe.model_validate(recipe).model_dump(mode="json")
                for recipe in recipes
            ],
        },
    )


@api.route("/")
@to_handleable_error
def get_paginations() -> Response:
    paginaged_recipes = crud_recipe.get_pagination()

    if paginaged_recipes.page != 1 and paginaged_recipes.page > paginaged_recipes.pages:
        abort(404)

    return jsonify(
        {
            "page": paginaged_recipes.page,
            "recipes": [
                Recipe.model_validate(recipe).model_dump(mode="json")
                for recipe in paginaged_recipes
            ],
            "total": paginaged_recipes.total,
            "per_page": config.PAGINATION_SIZE,
        },
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
