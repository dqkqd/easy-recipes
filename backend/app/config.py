import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEFAULT_INGREDIENT_IMAGE_NAME = "default-ingredient-image.jpg"
    DEFAULT_RECIPE_IMAGE_NAME = "default-recipe-image.jpg"

    # TODO(dqk): keeping them here for testing, remove after setting up docker
    DEFAULT_INGREDIENT_IMAGE = (
        BASE_DIR.parent / "static" / "images" / "default-ingredient-image.jpg"
    )
    DEFAULT_RECIPE_IMAGE = BASE_DIR.parent / "static" / "images" / "default-recipe-image.jpg"


class Config(BaseConfig):
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    FILE_SERVER_HOST = os.environ.get("FILE_SERVER_HOST")
    FILE_SERVER_PORT = os.environ.get("FILE_SERVER_PORT")
    FILE_SERVER_IMAGE_DIRECTORY = os.environ.get("FILE_SERVER_IMAGE_DIRECTORY")

    FILE_SERVER_URI = f"http://{FILE_SERVER_HOST}:{FILE_SERVER_PORT}/{FILE_SERVER_IMAGE_DIRECTORY}"

    DEFAULT_INGREDIENT_IMAGE_URI = f"{FILE_SERVER_URI}/{BaseConfig.DEFAULT_INGREDIENT_IMAGE}"
    DEFAULT_RECIPE_IMAGE_URI = f"{FILE_SERVER_URI}/{BaseConfig.DEFAULT_RECIPE_IMAGE}"


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    TEST_DB_PATH = os.environ.get("TEST_DB_PATH", "test.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{TEST_DB_PATH}"

    FILE_SERVER_URI = (BASE_DIR.parent / "static" / "images").as_uri()

    DEFAULT_INGREDIENT_IMAGE_URI = f"{FILE_SERVER_URI}/{BaseConfig.DEFAULT_INGREDIENT_IMAGE}"
    DEFAULT_RECIPE_IMAGE_URI = f"{FILE_SERVER_URI}/{BaseConfig.DEFAULT_RECIPE_IMAGE}"
