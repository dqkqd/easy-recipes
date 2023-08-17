import secrets

from app import constants


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(256)
    MAX_CONTENT_LENGTH = constants.MAX_CONTENT_LENGTH


class Config(BaseConfig):
    DATA_FOLDER_NAME = "data"
    IMAGE_FOLDER_NAME = "images"


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATA_FOLDER_NAME = "test_data"
    IMAGE_FOLDER_NAME = "test_images"
