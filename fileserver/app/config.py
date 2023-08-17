import secrets


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(256)

    STATIC_FOLDER = "static"
    DEFAULT_INGREDIENT_IMAGE = "default-ingredient-image.jpg"
    DEFAULT_RECIPE_IMAGE = "default-recipe-image.jpg"


class Config(BaseConfig):
    DATA_FOLDER_NAME = "data"
    IMAGE_FOLDER_NAME = "images"


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATA_FOLDER_NAME = "test_data"
    IMAGE_FOLDER_NAME = "test_images"
