from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, jsonify, request

from app.crud import crud_ingredient
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.schemas.ingredient import IngredientCreate, IngredientInDB

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
                ingredient.to_schema(IngredientInDB).to_public().model_dump(mode="json")
                for ingredient in ingredients
            ],
        },
    )


@api.route("/")
@to_handleable_error
def get_paginations() -> Response:
    paginaged_ingredients = crud_ingredient.get_pagination()
    return jsonify(
        {
            "page": paginaged_ingredients.page,
            "ingredients": [
                ingredient.to_schema(IngredientInDB).to_public().model_dump(mode="json")
                for ingredient in paginaged_ingredients
            ],
            "total": paginaged_ingredients.total,
        },
    )


@api.route("/<int:id>")
@to_handleable_error
def get_ingredient(id: int) -> Response:  # noqa: A002
    return jsonify(
        crud_ingredient.get(id)
        .to_schema(IngredientInDB)
        .to_public()
        .model_dump(mode="json"),
    )


@api.route("/", methods=["POST"])
@to_handleable_error
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
def delete_ingredient(id: int) -> Response:  # noqa: A002
    crud_ingredient.delete(id)
    return jsonify({"id": id})
