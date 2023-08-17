import json

from flask.testing import FlaskClient

from app import constants
from app.filename_handler import UniqueFilenameHandler


def test_get_default_ingredient(client: FlaskClient) -> None:
    response = client.get("/images/default/ingredient")
    assert response.status_code == 200
    assert constants.DEFAULT_INGREDIENT_IMAGE.read_bytes() == response.data


def test_get_default_recipe(client: FlaskClient) -> None:
    response = client.get("/images/default/recipe")
    assert response.status_code == 200
    assert constants.DEFAULT_RECIPE_IMAGE.read_bytes() == response.data


def test_upload_image(client: FlaskClient) -> None:
    files = {"file": constants.DEFAULT_RECIPE_IMAGE.open("rb")}
    response = client.post("/images/", data=files)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    handler = UniqueFilenameHandler.from_encrypted_filename(encrypted_filename)

    image_folder = client.application.config["IMAGE_FOLDER"]
    saved_file = image_folder / handler.filename
    assert saved_file.is_file()
