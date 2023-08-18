import json
import os
import shutil
from pathlib import Path

from cryptography.fernet import Fernet
from flask.testing import FlaskClient

from app import constants
from app.filename_handler import UniqueFilenameHandler


def test_200_get_default_image(client: FlaskClient) -> None:
    response = client.get("files/no-icon-image")
    assert response.status_code == 200
    assert constants.DEFAULT_IMAGE.read_bytes() == response.data


def test_200_upload_file(valid_password_token: str, tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data={"file": (file.open("rb"), "file.jpg")},
    )
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    # make sure there are no obvious connections between those filename
    assert encrypted_filename not in str(file)
    assert str(file) not in encrypted_filename

    key = client.application.config["FILE_SERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler.from_encrypted_filename(key, encrypted_filename)

    file_folder: Path = client.application.config["FILE_FOLDER"]
    saved_file = file_folder / handler.filename

    assert saved_file.is_file()
    assert not saved_file.samefile(file)
    assert saved_file.read_bytes() == file.read_bytes()


def test_422_upload_no_file(valid_password_token: str, client: FlaskClient) -> None:
    response = client.post("/files/", headers={"fs-token": valid_password_token})
    assert response.status_code == 400

    data = json.loads(response.data)
    assert data == {"message": "No file provided."}


def test_413_upload_too_large_file(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(constants.MAX_CONTENT_LENGTH))
    assert file.stat().st_size == constants.MAX_CONTENT_LENGTH

    files = {"file": file.open("rb")}
    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data=files,
    )
    assert response.status_code == 413

    data = json.loads(response.data)
    assert data == {"message": "File too large."}


def test_200_upload_big_file(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(constants.MAX_CONTENT_LENGTH - 1000))

    files = {"file": file.open("rb")}
    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data=files,
    )
    assert response.status_code == 200


def test_200_get_file(valid_password_token: str, tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data=files,
    )
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 200
    assert response.data == file.read_bytes()


def test_200_get_file_does_not_take_old_file(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    # make sure our file folder is empty
    file_folder: Path = client.application.config["FILE_FOLDER"]
    assert not os.listdir(file_folder)

    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data=files,
    )
    assert response.status_code == 200
    file_bytes = file.read_bytes()
    file.rename("new-file.jpg")

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 200
    assert response.data == file_bytes


def test_404_get_non_existed_file(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    # make sure our file folder is empty
    file_folder: Path = client.application.config["FILE_FOLDER"]
    assert not os.listdir(file_folder)

    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    files = {"file": file.open("rb")}
    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data=files,
    )
    assert response.status_code == 200

    shutil.rmtree(file_folder)

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 404


def test_404_get_file_no_filename_encrypted(client: FlaskClient) -> None:
    key = client.application.config["FILE_SERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler(key, "jpg")
    response = client.get(f"/files/{handler.encrypted_filename}")
    assert response.status_code == 404


def test_404_get_file_invalid_filename(client: FlaskClient) -> None:
    response = client.get("/files/123")
    assert response.status_code == 404


def test_500_get_file_with_wrong_key(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = client.post(
        "/files/",
        headers={"fs-token": valid_password_token},
        data={"file": file.open("rb")},
    )

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    # change to random key
    client.application.config["FILE_SERVER_ENCRYPT_KEY"] = Fernet.generate_key()
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 404


def test_500_get_file_invalid_key(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    always_valid_password_token = valid_password_token

    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = client.post(
        "/files/",
        headers={"fs-token": always_valid_password_token},
        data={"file": file.open("rb")},
    )

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    # change to random key
    client.application.config["FILE_SERVER_ENCRYPT_KEY"] = "invalid-key"
    response = client.get(f"/files/{encrypted_filename}")
    assert response.status_code == 500


def test_401_upload_file_no_password_token_provided(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = client.post("/files/", data={"file": file.open("rb")})
    assert response.status_code == 401

    data = json.loads(response.data)
    assert data == {"message": "Unauthorized."}


def test_401_upload_file_invalid_password(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = client.post(
        "/files/",
        headers={"fs-token": "invalid_password"},
        data={"file": file.open("rb")},
    )
    assert response.status_code == 401

    data = json.loads(response.data)
    assert data == {"message": "Unauthorized."}
