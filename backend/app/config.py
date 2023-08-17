from __future__ import annotations

import os


class BaseConfig:
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_port = os.environ.get("POSTGRES_PORT")
    postgres_db = os.environ.get("POSTGRES_DB")
    file_server_port = os.environ.get("FILE_SERVER_PORT")
    file_server_images_directory = os.environ.get("FILE_SERVER_IMAGES_DIRECTORY")
    default_ingredient_image_name = "default-ingredient-image.jpg"
    default_recipe_image_name = "default-recipe-image.jpg"
    postgres_host: str | None = None
    file_server_host: str | None = None

    @property
    def file_server_uri(self) -> str:
        return f"http://{self.file_server_host}:{self.file_server_port}/{self.file_server_images_directory}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa: N802
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def DEFAULT_INGREDIENT_IMAGE_URI(self) -> str:  # noqa: N802
        return f"{self.file_server_uri}/{self.default_ingredient_image_name}"

    @property
    def DEFAULT_RECIPE_IMAGE_URI(self) -> str:  # noqa: N802
        return f"{self.file_server_uri}/{self.default_recipe_image_name}"


class Config(BaseConfig):
    postgres_host = os.environ.get("POSTGRES_HOST")
    file_server_host = os.environ.get("FILE_SERVER_HOST")


class TestingConfig(BaseConfig):
    postgres_host = os.environ.get("TEST_POSTGRES_HOST")
    file_server_host = os.environ.get("TEST_FILE_SERVER_HOST")

    DEBUG = True
    TESTING = True
