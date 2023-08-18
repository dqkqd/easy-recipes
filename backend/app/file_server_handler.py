from __future__ import annotations

import io
import secrets
from functools import cached_property
from typing import TYPE_CHECKING, Self

import filetype
import requests
from cryptography.fernet import Fernet
from werkzeug import exceptions

if TYPE_CHECKING:
    from flask import Flask

FileIdentifer = str


def get_file_type_from_bytes(stream: io.BytesIO) -> filetype.Type:
    stream.seek(0)
    kind = filetype.guess(stream.read())
    stream.seek(0)
    if kind is None:
        raise TypeError
    return kind


class FileServer:
    timeout: float = 1

    def __init__(self) -> None:
        self._server_url: str | None = None

    def init_app(self, app: Flask) -> None:
        if "file_server" in app.extensions:
            raise RuntimeError("'FileServer' instance has already been registered")
        app.extensions["file_server"] = self

        file_server_url = app.config.get("FILE_SERVER_URL", None)
        if file_server_url is None:
            raise RuntimeError("FILE_SERVER_URL must be set")

        self._server_url = app.config["FILE_SERVER_URL"]

        self.authorization_scheme = app.config["FILE_SERVER_AUTHORIZATION_SCHEME"]
        self.encrypt_key = app.config["FILE_SERVER_ENCRYPT_KEY"]
        self.password = app.config["FILE_SERVER_PASSWORD"]
        self.fernet_model = Fernet(self.encrypt_key)

    @cached_property
    def server_url(self) -> str:
        if self._server_url is None:
            raise RuntimeError("FileServer object must `init_app` before used.")
        return self._server_url

    @cached_property
    def header(self) -> dict[str, str]:
        token = self.fernet_model.encrypt(self.password.encode()).decode()
        return {"Authorization": f"{self.authorization_scheme} {token}"}

    def uri(self, identifier: str) -> str:
        return f"{self.server_url}{identifier}"

    def get(self, identifier: str) -> io.BytesIO:
        uri = self.uri(identifier)
        r = requests.get(uri, timeout=self.timeout)
        return io.BytesIO(r.content)

    def add(self, filename: str, file_stream: io.BinaryIO) -> FileIdentifer:
        r = requests.post(
            self.server_url,
            headers=self.header,
            files={"file": (filename, file_stream)},
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)

        data = r.json()
        return data["filename"]

    def upload_image_from_url(self, url: str) -> str:
        raise NotImplementedError

    def upload_image_from_file(self, file: Path) -> FileIdentifer:
        checker = FileExtensionChecker.from_file(file)
        if not checker.is_image():
            raise TypeError(checker)
        return self.add(checker.random_filename, file.open("rb"))

    def upload_image_from_bytes(self, stream: io.BytesIO) -> FileIdentifer:
        checker = FileExtensionChecker.from_bytes_stream(stream)
        if not checker.is_image():
            raise TypeError(checker)
        return self.add(checker.random_filename, stream)


file_server = FileServer()
