from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, jsonify, request

from app.crud.ingredient import CRUDIngredient
from app.database import db
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.schemas.ingredient import IngredientCreate

if TYPE_CHECKING:
    from werkzeug import Response

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/")
@to_handleable_error
def get_ingredients() -> Response:
    msg = "TODO"
    raise NotImplementedError(msg)


@api.route("/<int:id>")
@to_handleable_error
def get_ingredient(id: int) -> Response:  # noqa: A002
    with CRUDIngredient.get_repository(db) as repo:
        ingredient_in_db = repo.get_by_id(id=id)
        return jsonify(ingredient_in_db.to_public().model_dump(mode="json"))


@api.route("/", methods=["POST"])
@to_handleable_error
def create_ingredient() -> Response:
    body = request.get_json()

    ingredient_create = IngredientCreate(**body)

    if ingredient_create.image_uri is not None:
        with ImageOnServer.from_source(ingredient_create.image_uri) as image_on_server:
            ingredient_create.image_uri = image_on_server.uri

    with CRUDIngredient.get_repository(db) as repo:
        ingredient_in_db = repo.create(ingredient_create)

    return jsonify({"id": ingredient_in_db.id})
