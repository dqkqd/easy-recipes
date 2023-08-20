from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, abort, jsonify, request

from app.crud import crud_recipe
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.schemas.recipe import RecipeCreate, RecipeInDB

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
                recipe.to_schema(RecipeInDB).to_public().model_dump(mode="json")
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
                recipe.to_schema(RecipeInDB).to_public().model_dump(mode="json")
                for recipe in paginaged_recipes
            ],
            "total": paginaged_recipes.total,
        },
    )


@api.route("/<int:id>")
@to_handleable_error
def get_recipe(id: int) -> Response:  # noqa: A002
    return jsonify(
        crud_recipe.get(id).to_schema(RecipeInDB).to_public().model_dump(mode="json"),
    )


@api.route("/", methods=["POST"])
@to_handleable_error
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
def delete_recipe(id: int) -> Response:  # noqa: A002
    crud_recipe.delete(id)
    return jsonify({"id": id})
