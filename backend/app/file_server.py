from __future__ import annotations

import io
from functools import cached_property
from typing import TYPE_CHECKING

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

    def uri(self, identifier: FileIdentifer) -> str:
        return f"{self.server_url}{identifier}"

    def get(self, identifier: FileIdentifer) -> io.BytesIO:
        uri = self.uri(identifier)
        return self._get_from_uri(uri)

    def add(self, source: str | io.BytesIO) -> FileIdentifer:
        if isinstance(source, io.BytesIO):
            return self._add_bytes(source)
        if isinstance(source, str):
            return self._add_url(source)
        raise NotImplementedError

    def delete(self, identifier: FileIdentifer) -> bool:
        uri = self.uri(identifier)
        response_identifier = self._delete_from_uri(uri)
        if response_identifier != identifier:
            raise exceptions.InternalServerError
        return True

    def _get_from_uri(self, uri: str) -> io.BytesIO:
        r = requests.get(uri, timeout=self.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return io.BytesIO(r.content)

    def _add_bytes(self, stream: io.BytesIO) -> FileIdentifer:
        file_type = get_file_type_from_bytes(stream)
        ext = file_type.extension

        r = requests.post(
            self.server_url,
            headers=self.header,
            files={"file": (f"file.{ext}", stream)},
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        data = r.json()
        return data["filename"]

    def _add_url(self, url: str) -> FileIdentifer:
        stream = self._get_from_uri(url)
        return self._add_bytes(stream)

    def _delete_from_uri(self, uri: str) -> FileIdentifer:
        r = requests.delete(
            uri,
            headers=self.header,
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        data = r.json()
        return data["filename"]


file_server = FileServer()
