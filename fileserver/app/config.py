import os
import secrets

from cryptography.fernet import Fernet


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(256)
    MAX_CONTENT_LENGTH = 1 * 1000 * 1000  # 1MB


class Config(BaseConfig):
    DATA_FOLDER_NAME = "data"
    FILE_FOLDER_NAME = "files"
    FILE_SERVER_ENCRYPT_KEY = os.environ.get("FILE_SERVER_ENCRYPT_KEY")
    FILE_SERVER_PASSWORD = os.environ.get("FILE_SERVER_PASSWORD")
    AUTHORIZATION_SCHEME = os.environ.get("FILE_SERVER_AUTHORIZATION_SCHEME")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATA_FOLDER_NAME = "test_data"
    FILE_FOLDER_NAME = "test_files"
    FILE_SERVER_ENCRYPT_KEY = Fernet.generate_key()
    FILE_SERVER_PASSWORD = "password"  # noqa: S105
    AUTHORIZATION_SCHEME = "FERNET_TOKEN"
