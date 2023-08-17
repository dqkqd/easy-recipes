from __future__ import annotations

from pathlib import Path

from flask import Flask

from app.config import Config


def setup_images_folder(app: Flask) -> None:
    image_folder: Path = (
        Path(app.root_path).parent
        / app.config["DATA_FOLDER_NAME"]
        / app.config["IMAGE_FOLDER_NAME"]
    )
    if not image_folder.exists():
        image_folder.mkdir()
    app.config["IMAGE_FOLDER"] = image_folder


def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__, static_folder=config.STATIC_FOLDER)
    app.config.from_object(config)

    setup_images_folder(app)

    from app.api import api

    app.register_blueprint(api)
    return app
