from flask import Blueprint, jsonify, request
from werkzeug import Response

from erecipes import models, schemas

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
def create_ingredient() -> Response:
    body = request.get_json()

    # @TODO(dqk): download and crop user upload image
    ingredient_base = schemas.IngredientBase(**body)
    ingredient_in_db = models.Ingredient(**ingredient_base.model_dump(mode="json"))
    ingredient_in_db.insert()

    return jsonify({"id": ingredient_in_db.id})
