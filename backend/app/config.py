from __future__ import annotations

import os
import secrets
from pathlib import Path

MAX_IMAGE_SIZE = 512
PAGINATION_SIZE = 12

DEFAULT_IMAGE_LOCATION = Path(__file__).parent / "static" / "images" / "no-image-icon.png"
if not DEFAULT_IMAGE_LOCATION.exists():
    raise FileNotFoundError


class BaseConfig:
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_port = os.environ.get("POSTGRES_PORT")
    postgres_db = os.environ.get("POSTGRES_DB")
    file_server_port = os.environ.get("FILE_SERVER_PORT")
    file_server_images_directory = os.environ.get("FILE_SERVER_IMAGES_DIRECTORY")
    default_ingredient_image_name = "default-ingredient-image.jpg"
    default_recipe_image_name = "default-recipe-image.jpg"
    postgres_host: str | None = None
    file_server_host: str | None = None

    DEBUG = int(os.environ.get("DEBUG", 0))

    FILE_SERVER_AUTHORIZATION_SCHEME = os.environ.get("FILE_SERVER_AUTHORIZATION_SCHEME")
    FILE_SERVER_ENCRYPT_KEY = os.environ.get("FILE_SERVER_ENCRYPT_KEY")
    FILE_SERVER_PASSWORD = os.environ.get("FILE_SERVER_PASSWORD")

    FILE_SERVER_REQUEST_TIMEOUT = float(
        os.environ.get("FILE_SERVER_REQUEST_TIMEOUT", 1.0),
    )

    @property
    def FILE_SERVER_URL(self) -> str:  # noqa: N802
        return f"http://{self.file_server_host}:{self.file_server_port}/"

    SECRET_KEY = secrets.token_urlsafe(256)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa: N802
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class Config(BaseConfig):
    postgres_host = os.environ.get("POSTGRES_HOST")
    file_server_host = os.environ.get("FILE_SERVER_HOST")


class TestingConfig(BaseConfig):
    postgres_host = os.environ.get("TEST_POSTGRES_HOST")
    file_server_host = os.environ.get("TEST_FILE_SERVER_HOST")

    DEBUG = True
    TESTING = True
