from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_from_directory
from werkzeug import exceptions

from app.auth import require_password
from app.errors import to_http_error
from app.filename_handler import UniqueFilenameHandler, secure_splitext

api = Blueprint("api", __name__)


@api.route("/<string:encrypted_filename>")
@to_http_error
def get_file(encrypted_filename: str) -> Response:
    file_folder = current_app.config["FILE_FOLDER"]
    if not isinstance(file_folder, Path):
        raise TypeError(file_folder)

    key = current_app.config["FILE_SERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler.from_encrypted_filename(key, encrypted_filename)
    file = file_folder / handler.filename
    if not file.exists():
        raise exceptions.NotFound

    return send_from_directory(
        file_folder,
        handler.filename,
    )


@api.route("/", methods=["POST"])
@to_http_error
@require_password
def upload_file() -> Response:
    """https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/"""
    file = request.files["file"]

    key = current_app.config["FILE_SERVER_ENCRYPT_KEY"]

    if file.filename is None:
        raise exceptions.UnsupportedMediaType

    _, ext = secure_splitext(file.filename)

    handler = UniqueFilenameHandler(key, ext)

    file_folder = current_app.config["FILE_FOLDER"]
    if not isinstance(file_folder, Path):
        raise TypeError(file_folder)
    file.save(file_folder / handler.filename)

    return jsonify({"filename": handler.encrypted_filename})


@api.route("/<string:encrypted_filename>", methods=["DELETE"])
@to_http_error
@require_password
def delete_file(encrypted_filename: str) -> Response:
    file_folder = current_app.config["FILE_FOLDER"]
    if not isinstance(file_folder, Path):
        raise TypeError(file_folder)

    key = current_app.config["FILE_SERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler.from_encrypted_filename(key, encrypted_filename)
    file = file_folder / handler.filename
    if not file.exists():
        raise exceptions.NotFound
    file.unlink()
    return jsonify({"filename": encrypted_filename})
