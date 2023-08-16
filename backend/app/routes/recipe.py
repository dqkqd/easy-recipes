from flask import Blueprint, jsonify
from werkzeug import Response

from app.models.database.orm import Recipe

api = Blueprint("recipes", __name__, url_prefix="/recipes")


@api.route("/")
def get_recipes() -> Response:
    # TODO(dqk): filter model's fields  # noqa: FIX002
    recipes = Recipe.query.all()
    return jsonify({"recipes": recipes})
