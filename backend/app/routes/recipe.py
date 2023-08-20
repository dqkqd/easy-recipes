from flask import Blueprint, jsonify
from werkzeug import Response

from app.models.recipe import Recipe

api = Blueprint("recipes", __name__, url_prefix="/recipes")


@api.route("/")
def get_recipes() -> Response:
    # TODO(dqk): filter model's fields
    recipes = Recipe.query.all()
    return jsonify({"recipes": recipes})
