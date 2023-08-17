from pathlib import Path

APP_DIR = Path(__file__).parent
STATIC_FOLDER = APP_DIR / "static"

DEFAULT_IMAGE_NAME = "no-image-icon.png"
DEFAULT_IMAGE = STATIC_FOLDER / DEFAULT_IMAGE_NAME

MAX_CONTENT_LENGTH = 1 * 1000 * 1000  # 1MB
