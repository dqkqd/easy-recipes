from flask import Blueprint, jsonify, request
from werkzeug import Response

from erecipes.models import Ingredient

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
def create_ingredient() -> Response:
    body = request.get_json()

    # @TODO(dqk): use pydantic model for validating
    # @TODO(dqk): validate url
    ingredient = Ingredient(**body)
    ingredient.insert()

    # @TODO(dqk): parse to json
    return jsonify({"ingredients": ingredient})
