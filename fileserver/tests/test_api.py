import json
from typing import TYPE_CHECKING

import pytest
from flask.testing import FlaskClient

from app import constants
from app.filename_handler import UniqueFilenameHandler

if TYPE_CHECKING:
    from pathlib import Path


def test_200_get_default_ingredient(client: FlaskClient) -> None:
    response = client.get("/images/default/ingredient")
    assert response.status_code == 200
    assert constants.DEFAULT_INGREDIENT_IMAGE.read_bytes() == response.data


def test_200_get_default_recipe(client: FlaskClient) -> None:
    response = client.get("/images/default/recipe")
    assert response.status_code == 200
    assert constants.DEFAULT_RECIPE_IMAGE.read_bytes() == response.data


def test_200_upload_image(client: FlaskClient) -> None:
    default_recipe_image = constants.DEFAULT_RECIPE_IMAGE
    files = {"file": default_recipe_image.open("rb")}
    response = client.post("/images/", data=files)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    handler = UniqueFilenameHandler.from_encrypted_filename(encrypted_filename)

    image_folder: Path = client.application.config["IMAGE_FOLDER"]
    saved_file = image_folder / handler.filename
    assert saved_file.is_file()
    assert not saved_file.samefile(default_recipe_image)
    assert saved_file.read_bytes() == default_recipe_image.read_bytes()


@pytest.mark.skip()
def test_200_upload_empty_image_would_use_default(client: FlaskClient) -> None:
    raise NotImplementedError


@pytest.mark.skip()
def test_200_upload_too_big_image(client: FlaskClient) -> None:
    raise NotImplementedError
