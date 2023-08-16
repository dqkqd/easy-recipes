import base64
from functools import cached_property
from io import BytesIO
from pathlib import Path
from typing import Self

from PIL import Image
from PIL.Image import Image as PillowImage


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
