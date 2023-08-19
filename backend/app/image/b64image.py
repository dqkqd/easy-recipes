import base64
import io
from contextlib import contextmanager
from functools import cached_property
from io import BytesIO
from pathlib import Path
from typing import Self

import requests
from PIL import Image
from PIL.Image import Image as PillowImage
from werkzeug import exceptions

from app import config
from app.file_server import fs
from app.file_server.core import FileIdentifer


class Base64Image:
    def __init__(self, encoded_data: bytes) -> None:
        self.encoded_data = encoded_data

    @cached_property
    def data(self) -> str:
        return self.encoded_data.decode("utf-8")

    @cached_property
    def image(self) -> PillowImage:
        decoded_data = base64.b64decode(self.encoded_data)
        return Image.open(BytesIO(decoded_data))

    @classmethod
    def from_image(cls, image: PillowImage) -> Self:
        raise NotImplementedError

    @classmethod
    def from_path(cls, path: Path) -> Self:
        encoded_data = base64.b64encode(path.read_bytes())
        return cls(encoded_data)

    @classmethod
    def from_url(cls, url: str) -> Self:
        raise NotImplementedError


def transform_image_stream(stream: io.BytesIO) -> io.BytesIO:
    image = Image.open(stream)
    image = crop_center(image)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
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
    def from_bytes(cls, stream: io.BytesIO) -> Self:
        try:
            image_bytes = transform_image_stream(stream)
        except Exception as e:  # noqa: BLE001 #TODO(dqk): remove hard code
            raise exceptions.UnsupportedMediaType("Invalid image") from e

        try:
            identifier = fs.add(image_bytes)
            yield cls(identifier)
        except Exception:
            fs.delete(identifier)
            raise

    @classmethod
    def from_file(cls, file: Path) -> Self:
        return cls.from_bytes(file.open("rb"))

    @classmethod
    def from_url(cls, url: str) -> Self:
        r = requests.get(url, timeout=cls.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return cls.from_bytes(io.BytesIO(r.content))
