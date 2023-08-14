from flask import Blueprint, jsonify
from werkzeug import Response

from erecipes.models import Recipe

api = Blueprint("recipes", __name__, url_prefix="/recipes")


@api.route("/")
def get_recipes() -> Response:
    # @TODO(dqk): filter model's fields
    recipes = Recipe.query.all()
    print(recipes)
    return jsonify({"recipes": recipes})
