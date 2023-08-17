from pathlib import Path

from flask import Blueprint, Response, current_app, send_from_directory

api = Blueprint("api", __name__)


@api.route("/images/<path:name>")
def get_image(name: Path) -> Response:
    return send_from_directory(
        current_app.config["IMAGE_FOLDER"],
        name,
        as_attachment=True,
    )


@api.route("/images/default/ingredient")
def get_default_ingredient_image() -> Response:
    return send_from_directory(
        current_app.static_folder,
        current_app.config["DEFAULT_INGREDIENT_IMAGE"],
    )


@api.route("/images/default/recipe")
def get_default_recipe_image() -> Response:
    return send_from_directory(
        current_app.static_folder,
        current_app.config["DEFAULT_RECIPE_IMAGE"],
    )
