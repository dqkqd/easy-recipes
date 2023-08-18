from __future__ import annotations

from pathlib import Path

from flask import Flask
from flask_cors import CORS

from app import constants
from app.config import BaseConfig, Config


def setup_files_folder(app: Flask) -> None:
    data_folder: Path = Path(app.root_path).parent / app.config["DATA_FOLDER_NAME"]
    if not data_folder.exists():
        data_folder.mkdir()
    app.config["DATA_FOLDER"] = data_folder

    file_folder: Path = data_folder / app.config["FILE_FOLDER_NAME"]
    if not file_folder.exists():
        file_folder.mkdir()
    app.config["FILE_FOLDER"] = file_folder


def create_app(config: type[BaseConfig] = Config) -> Flask:
    app = Flask(__name__, static_folder=constants.STATIC_FOLDER)
    app.config.from_object(config)

    CORS(app)

    setup_files_folder(app)

    from app.api import api

    app.register_blueprint(api)

    from app import errors

    app.register_error_handler(400, errors.no_uploaded_file)
    app.register_error_handler(404, errors.not_found)
    app.register_error_handler(422, errors.unprocessable)
    app.register_error_handler(413, errors.file_too_large)

    return app
