from flask import Blueprint, jsonify, request
from werkzeug import Response

from app.errors import catch_error
from app.models import orm, schema

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
@catch_error
def create_ingredient() -> Response:
    body = request.get_json()

    # @TODO(dqk): download and crop user upload image
    ingredient_base = schema.IngredientCreate(**body)
    ingredient_in_db = orm.Ingredient(**ingredient_base.model_dump(mode="json"))
    ingredient_in_db.insert()

    return jsonify({"id": ingredient_in_db.id})
