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
    if not os.path.isfile(DEFAULT_INGREDIENT_IMAGE):
        raise FileNotFoundError(DEFAULT_INGREDIENT_IMAGE)


class Config(BaseConfig):
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWD = os.environ.get("DB_PASSWD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TestingConfig(BaseConfig):
    TEST_DB_PATH = os.environ.get("TEST_DB_PATH")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{TEST_DB_PATH}"
