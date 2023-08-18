from __future__ import annotations

import io
from functools import cached_property
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from pathlib import Path

    from flask import Flask


class FileServer:
    timeout: float = 1

    def __init__(self) -> None:
        self._file_server_url: str | None = None

    def init_app(self, app: Flask) -> None:
        if "file_server" in app.extensions:
            raise RuntimeError("'FileServer' instance has already been registered")
        app.extensions["file_server"] = self

        file_server_url = app.config.get("FILE_SERVER_URL", None)
        if file_server_url is None:
            raise RuntimeError("FILE_SERVER_URL must be set")

        self._file_server_url = app.config["FILE_SERVER_URL"]

    @cached_property
    def file_server_url(self) -> str:
        if self._file_server_url is None:
            raise RuntimeError("FileServer object must `init_app` before used.")
        return self._file_server_url

    def image_url(self, identifier: str) -> str:
        if not isinstance(identifier, str):
            raise TypeError(identifier)
        return f"{self.file_server_url}{identifier}"

    def get_image(self, identifier: str) -> io.BytesIO:
        r = requests.get(self.image_url(identifier), timeout=self.timeout)
        return io.BytesIO(r.content)

    def upload_image_from_url(self, url: str) -> str:
        raise NotImplementedError

    def upload_image_from_file(self, file: Path) -> str:
        raise NotImplementedError

    def upload_image_from_bytes(self, b: io.BytesIO) -> str:
        raise NotImplementedError


file_server = FileServer()
