from flask import Blueprint, jsonify, request
from werkzeug import Response

from app.errors import to_handleable_error
from app.file_server.image import ImageOnServer
from app.models.database import db
from app.models.repositories.ingredient import IngredientRepository
from app.models.schemas import schema

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
        return jsonify(ingredient_in_db.model_dump(mode="json"))


@api.route("/", methods=["POST"])
@to_handleable_error
def create_ingredient() -> Response:
    body = request.get_json()

    ingredient_from_user = schema.IngredientFromUser(**body)
    with ImageOnServer.from_source(ingredient_from_user.image_url) as image_on_server:
        ingredient_create = schema.IngredientCreate(
            **ingredient_from_user.model_dump(exclude={"image_url"}),
            image_url=image_on_server.uri,
        )

    with IngredientRepository.get_repository(db) as repo:
        ingredient_in_db = repo.create_ingredient(ingredient_create)

    return jsonify({"id": ingredient_in_db.id})
