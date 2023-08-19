from __future__ import annotations

import io
from functools import cached_property, singledispatchmethod
from typing import TYPE_CHECKING, Any

import filetype
import requests
from cryptography.fernet import Fernet
from flask import current_app
from pydantic_core import Url
from werkzeug import exceptions

from app.errors import ServerAlreadyInitializedError, ServerConfigError, ServerDeleteWrongFileError

if TYPE_CHECKING:
    from flask import Flask

FileIdentifer = str


def get_file_type_from_bytes(stream: io.BytesIO | io.BufferedReader) -> filetype.Type:
    stream.seek(0)
    kind = filetype.guess(stream.read())
    stream.seek(0)
    if kind is None:
        raise TypeError(stream.read(32))
    return kind


class FileServer:
    def __init__(self, app: Flask | None = None) -> None:
        self._url: Url | None = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if "file_server" in app.extensions:
            raise ServerAlreadyInitializedError
        app.extensions["file_server"] = self

        try:
            server_url = app.config["FILE_SERVER_URL"]
            self._url = Url(server_url)

            self.timeout = app.config["FILE_SERVER_REQUEST_TIMEOUT"]
            self.authorization_scheme = app.config["FILE_SERVER_AUTHORIZATION_SCHEME"]
            self.encrypt_key = app.config["FILE_SERVER_ENCRYPT_KEY"]
            self.password = app.config["FILE_SERVER_PASSWORD"]
            self.fernet_model = Fernet(self.encrypt_key)
        except KeyError as e:
            raise ServerConfigError from e

    @cached_property
    def url(self) -> Url:
        if self._url is None:
            self.init_app(current_app)

        if self._url is None:
            raise ServerConfigError

        return self._url

    @cached_property
    def header(self) -> dict[str, str]:
        token = self.fernet_model.encrypt(self.password.encode()).decode()
        return {"Authorization": f"{self.authorization_scheme} {token}"}

    def file_uri(self, identifier: FileIdentifer) -> Url:
        return Url(f"{self.url}/{identifier}")

    def get(self, identifier: FileIdentifer) -> io.BytesIO:
        uri = self.file_uri(identifier)
        return self.get_from_uri(uri)

    def delete(self, identifier: FileIdentifer) -> bool:
        uri = self.file_uri(identifier)
        response_identifier = self.delete_from_uri(uri)
        if response_identifier != identifier:
            raise ServerDeleteWrongFileError
        return True

    @singledispatchmethod
    def add(self, source: Any) -> FileIdentifer:
        raise NotImplementedError(type(source))

    def get_from_uri(self, uri: Url) -> io.BytesIO:
        r = requests.get(str(uri), timeout=self.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return io.BytesIO(r.content)

    def delete_from_uri(self, uri: Url) -> FileIdentifer:
        r = requests.delete(
            str(uri),
            headers=self.header,
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)

        data = r.json()
        identifier = data["filename"]
        if not isinstance(identifier, FileIdentifer):
            # this error will never occur.
            raise TypeError(identifier)
        return identifier

    @add.register
    def _(self, stream: io.BytesIO | io.BufferedReader) -> FileIdentifer:
        try:
            file_type = get_file_type_from_bytes(stream)
        except TypeError as e:
            raise exceptions.UnsupportedMediaType("Invalid file.") from e
        ext = file_type.extension

        r = requests.post(
            str(self.url),
            headers=self.header,
            files={"file": (f"file.{ext}", stream)},
            timeout=self.timeout,
        )
        if r.status_code != 200:
            exceptions.abort(r.status_code)

        data = r.json()
        identifier = data["filename"]
        if not isinstance(identifier, FileIdentifer):
            # this error will never occur.
            raise TypeError(identifier)
        return identifier

    @add.register
    def _(self, url: Url) -> FileIdentifer:
        stream = self.get_from_uri(url)
        return self.add(stream)
