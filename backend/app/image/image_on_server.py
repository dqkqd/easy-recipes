from __future__ import annotations

import io
from contextlib import contextmanager
from functools import cached_property, singledispatchmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterator, Self

import requests
from PIL import Image
from pydantic_core import Url
from werkzeug import exceptions

from app.file_server import fs
from app.image.utils import transform_image_stream

if TYPE_CHECKING:
    from app.file_server.server import FileIdentifer


class ImageOnServer:
    def __init__(self, _identifier: FileIdentifer) -> None:
        self._identifier = _identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    def as_uri(self) -> Url:
        return fs.file_uri(self.identifier)

    @cached_property
    def byte_data(self) -> io.BytesIO:
        return fs.get(self.identifier)

    @cached_property
    def image(self) -> Image.Image:
        return Image.open(self.byte_data)

    @classmethod
    @contextmanager
    def from_source(cls, source: Any) -> Iterator[Self]:
        try:
            image_on_server = cls._from_source(source)
            yield image_on_server
        except Exception:
            fs.delete(image_on_server.identifier)
            raise

    @singledispatchmethod
    @classmethod
    def _from_source(cls, _source: Any) -> Self:
        raise NotImplementedError

    @_from_source.register
    @classmethod
    def _(cls, stream: io.BytesIO | io.BufferedReader) -> Self:
        image_bytes = transform_image_stream(stream)
        identifier = fs.add(image_bytes)
        return cls(identifier)

    @_from_source.register(Path)
    @classmethod
    def _(cls, file: Path) -> Self:
        return cls._from_source(file.open("rb"))

    @_from_source.register(Url)
    @classmethod
    def _(cls, url: Url) -> Self:
        r = requests.get(str(url), timeout=fs.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return cls._from_source(io.BytesIO(r.content))
