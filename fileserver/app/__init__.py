from __future__ import annotations

from pathlib import Path

from flask import Flask

from app import constants
from app.config import BaseConfig, Config


def setup_images_folder(app: Flask) -> None:
    data_folder: Path = Path(app.root_path).parent / app.config["DATA_FOLDER_NAME"]
    if not data_folder.exists():
        data_folder.mkdir()
    app.config["DATA_FOLDER"] = data_folder

    image_folder: Path = data_folder / app.config["IMAGE_FOLDER_NAME"]
    if not image_folder.exists():
        image_folder.mkdir()
    app.config["IMAGE_FOLDER"] = image_folder


def create_app(config: type[BaseConfig] = Config) -> Flask:
    app = Flask(__name__, static_folder=constants.STATIC_FOLDER)
    app.config.from_object(config)

    setup_images_folder(app)

    from app.api import api

    app.register_blueprint(api)

    from app.errors import not_found, unprocessable

    app.register_error_handler(404, not_found)
    app.register_error_handler(422, unprocessable)

    return app
