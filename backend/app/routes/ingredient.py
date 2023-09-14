from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, abort, jsonify, request

from app import auth, config
from app.crud import crud_ingredient
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.schemas.ingredient import Ingredient, IngredientCreate, IngredientUpdate

if TYPE_CHECKING:
    from werkzeug import Response

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/all")
@to_handleable_error
def get_ingredients() -> Response:
    ingredients = crud_ingredient.get_all()
    return jsonify(
        {
            "total": len(ingredients),
            "ingredients": [
                Ingredient.model_validate(ingredient).model_dump(mode="json")
                for ingredient in ingredients
            ],
        },
    )


@api.route("/")
@to_handleable_error
def get_paginations() -> Response:
    paginaged_ingredients = crud_ingredient.get_pagination(
        config.INGREDIENTS_PAGINATION_SIZE,
    )

    if (
        paginaged_ingredients.page != 1
        and paginaged_ingredients.page > paginaged_ingredients.pages
    ):
        abort(404)

    return jsonify(
        {
            "page": paginaged_ingredients.page,
            "ingredients": [
                Ingredient.model_validate(ingredient).model_dump(mode="json")
                for ingredient in paginaged_ingredients
            ],
            "total": paginaged_ingredients.total,
            "per_page": paginaged_ingredients.per_page,
        },
    )


@api.route("/<int:id>")
@to_handleable_error
def get_ingredient(id: int) -> Response:  # noqa: A002
    return jsonify(
        Ingredient.model_validate(
            crud_ingredient.get(id),
        ).model_dump(mode="json"),
    )


@api.route("/", methods=["POST"])
@to_handleable_error
@auth.require(auth.CREATE_INGREDIENT_PERMISSION)
def create_ingredient() -> Response:
    body = request.get_json()

    ingredient_create = IngredientCreate(**body)

    if ingredient_create.image_uri is not None:
        with ImageOnServer.from_source(ingredient_create.image_uri) as image_on_server:
            ingredient_create.image_uri = image_on_server.uri

    ingredient = crud_ingredient.add(ingredient_create)
    return jsonify({"id": ingredient.id})


@api.route("/<int:id>", methods=["DELETE"])
@to_handleable_error
@auth.require(auth.DELETE_INGREDIENT_PERMISSION)
def delete_ingredient(id: int) -> Response:  # noqa: A002
    crud_ingredient.delete(id)
    return jsonify({"id": id})


@api.route("/<int:id>", methods=["PATCH"])
@to_handleable_error
@auth.require(auth.UPDATE_INGREDIENT_PERMISSION)
def update_ingredient(id: int) -> Response:  # noqa: A002
    body = request.get_json()
    ingredient_update = IngredientUpdate(**body)

    if ingredient_update.image_uri is not None:
        with ImageOnServer.from_source(ingredient_update.image_uri) as image_on_server:
            ingredient_update.image_uri = image_on_server.uri

    ingredient_db = crud_ingredient.get(id=id)
    ingredient = crud_ingredient.update(ingredient_db, ingredient_update)
    return jsonify(Ingredient.model_validate(ingredient).model_dump(mode="json"))
