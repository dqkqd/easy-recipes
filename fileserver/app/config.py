import secrets

from app import constants


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(256)
    MAX_CONTENT_LENGTH = constants.MAX_CONTENT_LENGTH


class Config(BaseConfig):
    DATA_FOLDER_NAME = "data"
    FILE_FOLDER_NAME = "files"


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATA_FOLDER_NAME = "test_data"
    FILE_FOLDER_NAME = "test_files"
