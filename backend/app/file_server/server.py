from __future__ import annotations

import io
from functools import cached_property, singledispatchmethod
from typing import TYPE_CHECKING

import filetype  # type: ignore  # noqa: PGH003
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
    def __init__(self) -> None:
        self._url: str | None = None

    def init_app(self, app: Flask) -> None:
        if "file_server" in app.extensions:
            raise RuntimeError("'FileServer' instance has already been registered")
        app.extensions["file_server"] = self

        self._url = app.config["FILE_SERVER_URL"]

        self.timeout = app.config["FILE_SERVER_REQUEST_TIMEOUT"]

        self.authorization_scheme = app.config["FILE_SERVER_AUTHORIZATION_SCHEME"]
        self.encrypt_key = app.config["FILE_SERVER_ENCRYPT_KEY"]
        self.password = app.config["FILE_SERVER_PASSWORD"]

        self.fernet_model = Fernet(self.encrypt_key)

    @cached_property
    def url(self) -> str:
        if self._url is None:
            raise RuntimeError("FileServer object must `init_app` before used.")
        return self._url

    @cached_property
    def header(self) -> dict[str, str]:
        token = self.fernet_model.encrypt(self.password.encode()).decode()
        return {"Authorization": f"{self.authorization_scheme} {token}"}

    def file_uri(self, identifier: FileIdentifer) -> str:
        return f"{self.url}{identifier}"

    def get(self, identifier: FileIdentifer) -> io.BytesIO:
        uri = self.file_uri(identifier)
        return self._get_from_uri(uri)

    def delete(self, identifier: FileIdentifer) -> bool:
        uri = self.file_uri(identifier)
        response_identifier = self._delete_from_uri(uri)
        if response_identifier != identifier:
            raise exceptions.InternalServerError
        return True

    @singledispatchmethod
    def add(self, _source: str | io.BytesIO) -> FileIdentifer:
        raise NotImplementedError

    def _get_from_uri(self, uri: str) -> io.BytesIO:
        r = requests.get(uri, timeout=self.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return io.BytesIO(r.content)

    def _delete_from_uri(self, uri: str) -> FileIdentifer:
        r = requests.delete(
            uri,
            headers=self.header,
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)

        data = r.json()
        identifier = data["filename"]
        if not isinstance(identifier, FileIdentifer):
            raise TypeError(identifier)
        return identifier

    @add.register
    def _(self, stream: io.BytesIO) -> FileIdentifer:
        file_type = get_file_type_from_bytes(stream)
        ext = file_type.extension

        r = requests.post(
            self.url,
            headers=self.header,
            files={"file": (f"file.{ext}", stream)},
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)

        data = r.json()
        identifier = data["filename"]
        if not isinstance(identifier, FileIdentifer):
            raise TypeError(identifier)
        return identifier

    @add.register
    def _(self, url: str) -> FileIdentifer:
        stream = self._get_from_uri(url)
        return self.add(stream)
