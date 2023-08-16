import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEFAULT_INGREDIENT_IMAGE = (
        BASE_DIR.parent / "static" / "images" / "default-ingredient-image.jpg"
    )
    if not Path(DEFAULT_INGREDIENT_IMAGE).is_file():
        raise FileNotFoundError(DEFAULT_INGREDIENT_IMAGE)

    DEFAULT_RECIPE_IMAGE = BASE_DIR.parent / "static" / "images" / "default-recipe-image.jpg"
    if not Path(DEFAULT_RECIPE_IMAGE).is_file():
        raise FileNotFoundError(DEFAULT_RECIPE_IMAGE)


class Config(BaseConfig):
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    TEST_DB_PATH = os.environ.get("TEST_DB_PATH", "test.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{TEST_DB_PATH}"
