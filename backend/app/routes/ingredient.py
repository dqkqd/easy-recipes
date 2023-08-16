from flask import Blueprint, jsonify, request
from werkzeug import Response

from app.errors import catch_error
from app.models import schema
from app.models.database import db
from app.models.repositories.ingredient import IngredientRepository

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
@catch_error
def create_ingredient() -> Response:
    body = request.get_json()
    with IngredientRepository.get_repository(db) as repo:
        ingredient_create = schema.IngredientCreate(**body)
        ingredient_in_db = repo.create_ingredient(ingredient_create)
    return jsonify({"id": ingredient_in_db.id})
