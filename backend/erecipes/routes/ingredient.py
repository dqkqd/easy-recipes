from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from werkzeug import Response

from erecipes.errors import ERecipesError, catch_error
from erecipes.models import orm, schema

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
@catch_error
def create_ingredient() -> Response:
    body = request.get_json()

    # @TODO(dqk): download and crop user upload image
    try:
        ingredient_base = schema.IngredientCreate(**body)
    except ValidationError as exc:
        raise ERecipesError(f"Invalid {exc.errors()[0]['loc'][0]}.", 422) from exc

    ingredient_in_db = orm.Ingredient(**ingredient_base.model_dump(mode="json"))
    ingredient_in_db.insert()

    return jsonify({"id": ingredient_in_db.id})
