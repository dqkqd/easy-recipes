import os
import secrets

from cryptography.fernet import Fernet

from app import constants


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(256)
    MAX_CONTENT_LENGTH = constants.MAX_CONTENT_LENGTH


class Config(BaseConfig):
    DATA_FOLDER_NAME = "data"
    FILE_FOLDER_NAME = "files"
    FILESERVER_ENCRYPT_KEY = os.environ.get("FILESERVER_ENCRYPT_KEY")
    FILESERVER_PASSWORD = os.environ.get("FILESEVER_PASSWORD")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATA_FOLDER_NAME = "test_data"
    FILE_FOLDER_NAME = "test_files"
    FILESERVER_ENCRYPT_KEY = Fernet.generate_key()
    FILESERVER_PASSWORD = "password"  # noqa: S105
