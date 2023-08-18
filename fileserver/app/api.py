from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_from_directory
from werkzeug import exceptions

from app import constants
from app.errors import to_http_error
from app.filename_handler import UniqueFilenameHandler

api = Blueprint("api", __name__, url_prefix="/files")


@api.route("/<string:encrypted_filename>")
@to_http_error
def get_file(encrypted_filename: str) -> Response:
    file_folder = current_app.config["FILE_FOLDER"]
    if not isinstance(file_folder, Path):
        raise TypeError(file_folder)

    handler = UniqueFilenameHandler.from_encrypted_filename(encrypted_filename)
    file = file_folder / handler.filename
    if not file.exists():
        raise exceptions.NotFound(file)

    return send_from_directory(
        file_folder,
        handler.filename,
        as_attachment=True,
    )


@api.route("/no-icon-image")
@to_http_error
def get_default_image() -> Response:
    return send_from_directory(
        constants.STATIC_FOLDER,
        constants.DEFAULT_IMAGE_NAME,
    )


@api.route("/", methods=["POST"])
@to_http_error
def upload_file() -> Response:
    """https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/"""
    file = request.files["file"]
    handler = UniqueFilenameHandler()

    file_folder = current_app.config["FILE_FOLDER"]
    if not isinstance(file_folder, Path):
        raise TypeError(file_folder)
    file.save(file_folder / handler.filename)

    return jsonify({"filename": handler.encrypted_filename})
