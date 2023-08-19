from __future__ import annotations

import shutil
from typing import TYPE_CHECKING, Iterator

import pytest
from cryptography.fernet import Fernet

from app import create_app
from app.config import TestingConfig

if TYPE_CHECKING:
    from pathlib import Path

    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@pytest.fixture()
def app() -> Iterator[Flask]:
    app = create_app(TestingConfig)

    yield app

    data_folder: Path = app.config["DATA_FOLDER"]
    if data_folder.exists():
        shutil.rmtree(data_folder)


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def valid_password_token(app: Flask) -> str:
    password = app.config["FILE_SERVER_PASSWORD"]
    fernet_model = Fernet(app.config["FILE_SERVER_ENCRYPT_KEY"])
    return fernet_model.encrypt(password.encode()).decode()


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
