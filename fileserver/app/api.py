from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_from_directory

from app import utils

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


@api.route("/images/", methods=["POST"])
def upload_image() -> Response:
    """https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/"""
    if "file" not in request.files:
        msg = "file does not exist"
        raise KeyError(msg)

    file = request.files["file"]
    if file.filename.strip() == "":
        msg = "Invalid filename."
        raise ValueError(msg)

    if file and utils.allowed_file(file.filename):
        filename = utils.encode_filename(file.filename)
        # TODO(dqk): convert filename
        # TODO(dqk): separate file between ingredient and recipe
        file.save(current_app.config["IMAGE_FOLDER"] / filename)

    return jsonify({"filename": filename})
