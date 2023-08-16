from flask import Blueprint, jsonify, request
from werkzeug import Response

from app.errors import to_handleable_error
from app.models.database import db
from app.models.repositories.ingredient import IngredientRepository
from app.models.schemas import schema

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
@to_handleable_error
def create_ingredient() -> Response:
    body = request.get_json()
    with IngredientRepository.get_repository(db) as repo:
        ingredient_create = schema.IngredientCreate(**body)
        ingredient_in_db = repo.create_ingredient(ingredient_create)
    return jsonify({"id": ingredient_in_db.id})
