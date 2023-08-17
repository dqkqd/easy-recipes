from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_from_directory

from app.filename_handler import UniqueFilenameHandler

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
    handler = UniqueFilenameHandler()

    # TODO(dqk): separate file between ingredient and recipe
    file.save(current_app.config["IMAGE_FOLDER"] / handler.filename)

    return jsonify({"filename": handler.encrypted_filename})
