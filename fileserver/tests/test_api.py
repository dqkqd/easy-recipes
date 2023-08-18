import json
import os
from pathlib import Path

from flask.testing import FlaskClient

from app import constants
from app.filename_handler import UniqueFilenameHandler


def test_200_get_default_image(client: FlaskClient) -> None:
    response = client.get("files/no-icon-image")
    assert response.status_code == 200
    assert constants.DEFAULT_IMAGE.read_bytes() == response.data


def test_200_upload_file(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post("/files/", data=files)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    # make sure there are no obvious connections between those filename
    assert encrypted_filename not in str(file)
    assert str(file) not in encrypted_filename

    key = client.application.config["FILESERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler.from_encrypted_filename(key, encrypted_filename)

    file_folder: Path = client.application.config["FILE_FOLDER"]
    saved_file = file_folder / handler.filename

    assert saved_file.is_file()
    assert not saved_file.samefile(file)
    assert saved_file.read_bytes() == file.read_bytes()


def test_422_upload_no_file(client: FlaskClient) -> None:
    response = client.post("/files/")
    assert response.status_code == 400

    data = json.loads(response.data)
    assert data == {"message": "No file provided."}


def test_413_upload_too_large_file(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(constants.MAX_CONTENT_LENGTH))
    assert file.stat().st_size == constants.MAX_CONTENT_LENGTH

    files = {"file": file.open("rb")}
    response = client.post("/files/", data=files)
    assert response.status_code == 413

    data = json.loads(response.data)
    assert data == {"message": "File too large."}


def test_200_upload_big_file(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(constants.MAX_CONTENT_LENGTH - 1000))

    files = {"file": file.open("rb")}
    response = client.post("/files/", data=files)
    assert response.status_code == 200


def test_200_get_file(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post("/files/", data=files)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 200
    assert response.data == file.read_bytes()


def test_200_get_file_does_not_take_old_file(tmp_path: Path, client: FlaskClient) -> None:
    # make sure our file folder is empty
    file_folder: Path = client.application.config["FILE_FOLDER"]
    assert not os.listdir(file_folder)

    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post("/files/", data=files)
    assert response.status_code == 200
    file_bytes = file.read_bytes()
    file.rename("new-file.txt")

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 200
    assert response.data == file_bytes


def test_404_get_non_existed_file(tmp_path: Path, client: FlaskClient) -> None:
    # make sure our file folder is empty
    file_folder: Path = client.application.config["FILE_FOLDER"]
    assert not os.listdir(file_folder)

    file = tmp_path / "file.txt"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post("/files/", data=files)
    assert response.status_code == 200

    for file in os.listdir(file_folder):
        (file_folder / file).unlink()

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 404


def test_404_get_file_no_filename_encrypted(client: FlaskClient) -> None:
    key = client.application.config["FILESERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler(key)
    response = client.get(f"/files/{handler.encrypted_filename}")
    assert response.status_code == 404
