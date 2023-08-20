from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Blueprint, jsonify, request

from app.database import db
from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.repositories.ingredient import IngredientRepository
from app.schemas.ingredient import IngredientBase, IngredientCreate

if TYPE_CHECKING:
    from pydantic import HttpUrl
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
    with IngredientRepository.get_repository(db) as repo:
        ingredient_in_db = repo.get_ingredient(id=id)
        return jsonify(ingredient_in_db.to_public().model_dump(mode="json"))


@api.route("/", methods=["POST"])
@to_handleable_error
def create_ingredient() -> Response:
    body = request.get_json()

    ingredient_from_user = IngredientBase(**body)

    image_uri: HttpUrl | None = None
    if ingredient_from_user.image_uri is not None:
        with ImageOnServer.from_source(ingredient_from_user.image_uri) as image_on_server:
            image_uri = image_on_server.uri

    ingredient_create = IngredientCreate(
        **ingredient_from_user.model_dump(exclude={"image_uri"}),
        image_uri=image_uri,
    )

    with IngredientRepository.get_repository(db) as repo:
        ingredient_in_db = repo.create_ingredient(ingredient_create)

    return jsonify({"id": ingredient_in_db.id})
