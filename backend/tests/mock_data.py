from __future__ import annotations

import io
import uuid
from typing import TYPE_CHECKING, Any

import numpy as np
from PIL import Image

from app.file_server.image import ImageOnServer
from app.schemas.ingredient import IngredientCreate

if TYPE_CHECKING:
    from pydantic_core import Url


def random_id() -> str:
    return uuid.uuid4().hex


class MockImage:
    @staticmethod
    def random_image(w: int, h: int) -> Image.Image:
        rng = np.random.default_rng(seed=42)
        image_data = rng.random((w, h, 3)) * 255
        return Image.fromarray(image_data.astype("uint8")).convert("RGB")

    @staticmethod
    def random_image_bytes(w: int, h: int) -> io.BytesIO:
        image = MockImage.random_image(w, h)
        stream = io.BytesIO()
        image.save(stream, format="PNG")
        return stream

    @staticmethod
    def random_valid_image_uri(w: int, h: int) -> Url:
        with ImageOnServer.from_source(
            MockImage.random_image_bytes(w, h),
        ) as image_on_server:
            return image_on_server.uri


class MockIngredient:
    @staticmethod
    def random_valid_ingredient() -> IngredientCreate:
        return IngredientCreate(
            name=random_id(),
            image_uri=MockImage.random_valid_image_uri(50, 50),
        )

    @staticmethod
    def random_valid_ingredient_data() -> dict[str, Any]:
        return MockIngredient.random_valid_ingredient().model_dump(mode="json")
