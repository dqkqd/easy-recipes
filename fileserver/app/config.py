import os
import secrets

from cryptography.fernet import Fernet


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(256)


class Config(BaseConfig):
    DATA_FOLDER_NAME = "data"
    FILE_FOLDER_NAME = "files"
    FILE_SERVER_ENCRYPT_KEY = os.environ.get("FILE_SERVER_ENCRYPT_KEY")
    FILE_SERVER_PASSWORD = os.environ.get("FILE_SERVER_PASSWORD")
    AUTHORIZATION_SCHEME = os.environ.get("FILE_SERVER_AUTHORIZATION_SCHEME")
    FILE_SERVER_REQUEST_TIMEOUT = os.environ.get("FILE_SERVER_REQUEST_TIMEOUT")
    MAX_CONTENT_LENGTH = os.environ.get("FILE_SERVER_MAX_CONTENT_LENGTH")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATA_FOLDER_NAME = "test_data"
    FILE_FOLDER_NAME = "test_files"
    FILE_SERVER_ENCRYPT_KEY = Fernet.generate_key()
    FILE_SERVER_PASSWORD = "password"  # noqa: S105
    AUTHORIZATION_SCHEME = "FERNET_TOKEN"
    FILE_SERVER_REQUEST_TIMEOUT = 1.5
    MAX_CONTENT_LENGTH = 1 * 1000 * 1000  # 1MB
