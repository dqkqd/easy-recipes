from __future__ import annotations

import json
import os
import shutil
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet

from app.filename_handler import UniqueFilenameHandler

if TYPE_CHECKING:
    from pathlib import Path

    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def upload_file(
    client: FlaskClient,
    file: Path | None,
    *,
    password_token: str | None = None,
) -> TestResponse:
    authorization_scheme = client.application.config["AUTHORIZATION_SCHEME"]

    headers = {}
    if password_token is not None:
        headers = {"Authorization": f"{authorization_scheme} {password_token}"}

    if file is not None:
        data = {"file": (file.open("rb"), "file.jpg")}
        return client.post("/", headers=headers, data=data)
    return client.post("/", headers=headers)


def delete_file(
    client: FlaskClient,
    encrypted_filename: str,
    password_token: str | None = None,
) -> TestResponse:
    authorization_scheme = client.application.config["AUTHORIZATION_SCHEME"]
    return client.delete(
        f"/{encrypted_filename}",
        headers={"Authorization": f"{authorization_scheme} {password_token}"},
    )


def test_200_upload_file(valid_password_token: str, tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    response = upload_file(client, file=file, password_token=valid_password_token)
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
    response = upload_file(client, file=None, password_token=valid_password_token)
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
        f.write(bytearray(client.application.config["MAX_CONTENT_LENGTH"]))
    assert file.stat().st_size == client.application.config["MAX_CONTENT_LENGTH"]

    response = upload_file(client, file=file, password_token=valid_password_token)
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
        f.write(bytearray(client.application.config["MAX_CONTENT_LENGTH"] - 1000))

    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 200


def test_200_get_file(valid_password_token: str, tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/{encrypted_filename}")
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

    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 200
    file_bytes = file.read_bytes()
    file.rename("new-file.jpg")

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/{encrypted_filename}")
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

    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 200

    shutil.rmtree(file_folder)

    data = json.loads(response.data)
    encrypted_filename = data["filename"]
    response = client.get(f"/{encrypted_filename}")
    assert response.status_code == 404


def test_404_get_file_no_filename_encrypted(client: FlaskClient) -> None:
    key = client.application.config["FILE_SERVER_ENCRYPT_KEY"]
    handler = UniqueFilenameHandler(key, "jpg")
    response = client.get(f"/{handler.encrypted_filename}")
    assert response.status_code == 404


def test_404_get_file_invalid_filename(client: FlaskClient) -> None:
    response = client.get("/123")
    assert response.status_code == 404


def test_500_get_file_with_wrong_key(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token=valid_password_token)

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    # change to random key
    client.application.config["FILE_SERVER_ENCRYPT_KEY"] = Fernet.generate_key()
    response = client.get(f"/{encrypted_filename}")
    assert response.status_code == 404


def test_500_get_file_invalid_key(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token=valid_password_token)

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    # change to random key
    client.application.config["FILE_SERVER_ENCRYPT_KEY"] = "invalid-key"
    response = client.get(f"/{encrypted_filename}")
    assert response.status_code == 500


def test_401_upload_file_no_password_token_provided(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token=None)
    assert response.status_code == 401

    data = json.loads(response.data)
    assert data == {"message": "Unauthorized."}


def test_401_upload_file_invalid_password(tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token="invalid-password")  # noqa: S106
    assert response.status_code == 401

    data = json.loads(response.data)
    assert data == {"message": "Unauthorized."}


def test_401_upload_file_wrong_key(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    client.application.config["FILE_SERVER_ENCRYPT_KEY"] = Fernet.generate_key()
    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 401

    client.application.config["FILE_SERVER_ENCRYPT_KEY"] = "invalid-key"
    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 401


def test_200_delete_file(valid_password_token: str, tmp_path: Path, client: FlaskClient) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token=valid_password_token)

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    response = client.get(f"/{encrypted_filename}")
    assert response.status_code == 200

    response = delete_file(client, encrypted_filename, valid_password_token)
    assert response.status_code == 200

    response = client.get(f"/{encrypted_filename}")
    assert response.status_code == 404


def test_404_delete_file_twice(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token=valid_password_token)

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    response = delete_file(client, encrypted_filename, valid_password_token)
    assert response.status_code == 200

    response = delete_file(client, encrypted_filename, valid_password_token)
    assert response.status_code == 404


def test_401_delete_file_invalid_password(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))
    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 200

    data = json.loads(response.data)
    encrypted_filename = data["filename"]

    response = delete_file(
        client,
        encrypted_filename,
        password_token="invalid-password-token",  # noqa: S106
    )
    assert response.status_code == 401
