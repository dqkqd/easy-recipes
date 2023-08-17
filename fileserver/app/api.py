from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_from_directory

from app import constants
from app.errors import to_http_error
from app.filename_handler import UniqueFilenameHandler

image_api = Blueprint("api", __name__, url_prefix="/images")


@image_api.route("/<string:encrypted_filename>")
@to_http_error
def get_image(encrypted_filename: str) -> Response:
    image_folder = current_app.config["IMAGE_FOLDER"]
    if not isinstance(image_folder, Path):
        raise TypeError(image_folder)

    handler = UniqueFilenameHandler.from_encrypted_filename(encrypted_filename)
    file = image_folder / handler.filename
    if not file.exists():
        raise FileNotFoundError(file)

    return send_from_directory(
        image_folder,
        handler.filename,
        as_attachment=True,
    )


@image_api.route("/default")
@to_http_error
def get_default_image() -> Response:
    return send_from_directory(
        constants.STATIC_FOLDER,
        constants.DEFAULT_IMAGE_NAME,
    )


@image_api.route("/", methods=["POST"])
@to_http_error
def upload_image() -> Response:
    """https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/"""
    file = request.files["file"]
    handler = UniqueFilenameHandler()

    image_folder = current_app.config["IMAGE_FOLDER"]
    if not isinstance(image_folder, Path):
        raise TypeError(image_folder)
    file.save(image_folder / handler.filename)

    return jsonify({"filename": handler.encrypted_filename})
