from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

FILE_SERVER_PORT = os.environ.get("FILE_SERVER_PORT")
FILE_SERVER_IMAGES_DIRECTORY = os.environ.get("FILE_SERVER_IMAGES_DIRECTORY")


DEFAULT_INGREDIENT_IMAGE_NAME = "default-ingredient-image.jpg"
DEFAULT_RECIPE_IMAGE_NAME = "default-recipe-image.jpg"


class BaseConfig:
    POSTGRES_HOST: str | None = None
    FILE_SERVER_HOST: str | None = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa: N802
        return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    @property
    def FILE_SERVER_URI(self) -> str:  # noqa: N802
        return f"http://{self.FILE_SERVER_HOST}:{FILE_SERVER_PORT}/{FILE_SERVER_IMAGES_DIRECTORY}"

    @property
    def DEFAULT_INGREDIENT_IMAGE_URI(self) -> str:  # noqa: N802
        return f"{self.FILE_SERVER_URI}/{DEFAULT_INGREDIENT_IMAGE_NAME}"

    @property
    def DEFAULT_RECIPE_IMAGE_URI(self) -> str:  # noqa: N802
        return f"{self.FILE_SERVER_URI}/{DEFAULT_RECIPE_IMAGE_NAME}"


class Config(BaseConfig):
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    FILE_SERVER_HOST = os.environ.get("FILE_SERVER_HOST")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    POSTGRES_HOST = os.environ.get("TEST_POSTGRES_HOST")
    FILE_SERVER_HOST = os.environ.get("TEST_FILE_SERVER_HOST")
