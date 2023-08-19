import base64
import io
from functools import cached_property
from io import BytesIO
from pathlib import Path
from typing import Self

import requests
from PIL import Image
from PIL.Image import Image as PillowImage
from werkzeug import exceptions

from app import config
from app.file_server.core import FileIdentifer, FileServer


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


class ImageHandler:
    timeout: float = 1.0

    def __init__(self, image: Image, raw: bool) -> None:  # noqa: FBT001
        self.image = image
        self.raw = raw

    @classmethod
    def from_bytes(cls, stream: io.BytesIO) -> Self:
        try:
            return cls(Image.open(stream), raw=True)
        except Exception as e:  # noqa: BLE001 #TODO(dqk): remove hard code
            raise exceptions.UnsupportedMediaType("Invalid image") from e

    @classmethod
    def from_file(cls, file: Path) -> Self:
        return cls.from_bytes(file.open("rb"))

    @classmethod
    def from_url(cls, url: str) -> Self:
        r = requests.get(url, timeout=cls.timeout)
        if r.status_code != 200:
            exceptions.abort(r.status_code)
        return cls.from_bytes(io.BytesIO(r.content))

    def crop_center(self) -> None:
        w, h = self.image.size
        crop_size = min(max(w, h), config.MAX_IMAGE_SIZE)
        self.image = self.image.crop(
            (w - crop_size) // 2,
            (h - crop_size) // 2,
            (w + crop_size) // 2,
            (h - crop_size) // 2,
        )
        self.raw = False

    @property
    def stream(self) -> io.BytesIO:
        if not self.raw:
            self.crop_center()
        image_bytes = io.BytesIO()
        self.image.save(image_bytes, format="PNG")
        return image_bytes

    def upload(self, file_server: FileServer) -> FileIdentifer:
        return file_server.add(self.stream)
