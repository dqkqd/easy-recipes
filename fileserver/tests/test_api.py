import json
from pathlib import Path

from flask.testing import FlaskClient

from app import constants
from app.filename_handler import UniqueFilenameHandler


def test_200_get_default_image(client: FlaskClient) -> None:
    response = client.get("/images/default")
    assert response.status_code == 200
    assert constants.DEFAULT_IMAGE.read_bytes() == response.data


def test_200_upload_image(client: FlaskClient) -> None:
    default_image = constants.DEFAULT_IMAGE
    files = {"file": default_image.open("rb")}
    response = client.post("/images/", data=files)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    handler = UniqueFilenameHandler.from_encrypted_filename(encrypted_filename)

    image_folder: Path = client.application.config["IMAGE_FOLDER"]
    saved_file = image_folder / handler.filename
    assert saved_file.is_file()
    assert not saved_file.samefile(default_image)
    assert saved_file.read_bytes() == default_image.read_bytes()


def test_422_upload_no_image(client: FlaskClient) -> None:
    response = client.post("/images/")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"message": "No image provided."}


def test_413_upload_too_big_image(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(constants.MAX_CONTENT_LENGTH + 1))
    assert file.stat().st_size == constants.MAX_CONTENT_LENGTH + 1

    files = {"file": file.open("rb")}
    response = client.post("/images/", data=files)
    assert response.status_code == 413

    data = json.loads(response.data)
    assert data == {"message": "File too large."}


def test_200_upload_big_image(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(constants.MAX_CONTENT_LENGTH - 300))
    files = {"file": file.open("rb")}
    response = client.post("/images/", data=files)
    assert response.status_code == 200
