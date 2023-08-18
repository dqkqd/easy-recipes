import os
from pathlib import Path

from cryptography.fernet import Fernet

APP_DIR = Path(__file__).parent
STATIC_FOLDER = APP_DIR / "static"

DEFAULT_IMAGE_NAME = "no-image-icon.png"
DEFAULT_IMAGE = STATIC_FOLDER / DEFAULT_IMAGE_NAME

MAX_CONTENT_LENGTH = 1 * 1000 * 1000  # 1MB

FILESERVER_ENCRYPT_KEY = os.environ.get("FILESERVER_ENCRYPT_KEY", Fernet.generate_key())
FILESERVER_PASSWORD = os.environ.get("FILESEVER_PASSWORD", "password")
