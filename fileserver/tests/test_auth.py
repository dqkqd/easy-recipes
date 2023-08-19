import json
import time
from pathlib import Path

from cryptography.fernet import Fernet
from flask.testing import FlaskClient

from tests.conftest import upload_file


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

    client.application.config.pop("FILE_SERVER_ENCRYPT_KEY")
    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 401


def test_401_upload_file_after_timeout(
    valid_password_token: str,
    tmp_path: Path,
    client: FlaskClient,
) -> None:
    file = tmp_path / "file.jpg"
    with file.open("wb") as f:
        f.write(bytearray(1000))

    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 200

    time.sleep(client.application.config["FILE_SERVER_REQUEST_TIMEOUT"] * 1.5)

    response = upload_file(client, file=file, password_token=valid_password_token)
    assert response.status_code == 401


def test_200_get_file_after_timeout(
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

    time.sleep(client.application.config["FILE_SERVER_REQUEST_TIMEOUT"] * 1.5)
    response = client.get(f"/{encrypted_filename}")
    assert response.status_code == 200
