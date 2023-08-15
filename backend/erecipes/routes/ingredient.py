from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from werkzeug import Response

from erecipes import models, schemas
from erecipes.errors import ERecipesError, catch_error

api = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@api.route("/", methods=["POST"])
@catch_error
def create_ingredient() -> Response:
    body = request.get_json()

    # @TODO(dqk): download and crop user upload image
    try:
        ingredient_base = schemas.IngredientBase(**body)
    except ValidationError as exc:
        raise ERecipesError(f"Invalid {exc.errors()[0]['loc'][0]}.", 422) from exc

    ingredient_in_db = models.Ingredient(**ingredient_base.model_dump(mode="json"))
    ingredient_in_db.insert()

    return jsonify({"id": ingredient_in_db.id})
