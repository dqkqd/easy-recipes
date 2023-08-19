from __future__ import annotations

import io
from contextlib import contextmanager
from functools import cached_property
from typing import TYPE_CHECKING, Iterator, Self

import requests
from PIL import Image
from werkzeug import exceptions

from app import config
from app.file_server import fs

if TYPE_CHECKING:
    from pathlib import Path

    from app.file_server.core import FileIdentifer


def transform_image_stream(stream: io.BytesIO | io.BufferedReader) -> io.BytesIO:
    try:
        image = Image.open(stream)
        image = crop_center(image)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
    except Exception as e:  # noqa: BLE001 #TODO(dqk): remove hard code
        raise exceptions.UnsupportedMediaType("Invalid image") from e
    else:
        return image_bytes


def crop_center(image: Image.Image) -> Image.Image:
    w, h = image.size
    crop_size = min(max(w, h), config.MAX_IMAGE_SIZE)
    return image.crop(
        (
            (w - crop_size) // 2,
            (h - crop_size) // 2,
            (w + crop_size) // 2,
            (h + crop_size) // 2,
        ),
    )


class ImageOnServer:
    timeout: float = 1.0

    def __init__(self, _identifier: FileIdentifer) -> None:
        self._identifier = _identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    def as_uri(self) -> str:
        return fs.uri(self.identifier)

    @cached_property
    def byte_data(self) -> io.BytesIO:
        return fs.get(self.identifier)

    @cached_property
    def image(self) -> Image.Image:
        return Image.open(self.byte_data)

    @classmethod
    @contextmanager
    def from_bytes(cls, stream: io.BytesIO | io.BufferedReader) -> Iterator[Self]:
        image_bytes = transform_image_stream(stream)

        try:
            identifier = fs.add(image_bytes)
            yield cls(identifier)
        except Exception:
            fs.delete(identifier)
            raise

    @classmethod
    @contextmanager
    def from_file(cls, file: Path) -> Iterator[Self]:
        with cls.from_bytes(file.open("rb")) as img:
            yield img

    @classmethod
    @contextmanager
    def from_url(cls, url: str) -> Iterator[Self]:
        r = requests.get(url, timeout=cls.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        with cls.from_bytes(io.BytesIO(r.content)) as img:
            yield img
