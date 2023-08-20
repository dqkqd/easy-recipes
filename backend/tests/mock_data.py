from __future__ import annotations

import io
import secrets
from typing import Any

import numpy as np
from PIL import Image
from pydantic_core import Url

from app.file_server.image import ImageOnServer
from app.schemas import schema


def random_str(length: int = 5) -> str:
    return secrets.token_urlsafe(length)


def random_valid_url() -> Url:
    return Url(f"http://{random_str(10)}.com/{random_str(10)}")


def ingredient_create_data(name: str | None = None) -> dict[str, Any]:
    ingredient = schema.IngredientCreate(
        name=name if name is not None else random_str(),
        image_uri=random_valid_url(),
    )
    return ingredient.model_dump(mode="json")


def random_image(w: int, h: int) -> Image.Image:
    rng = np.random.default_rng(seed=42)
    image_data = rng.random((w, h, 3)) * 255
    return Image.fromarray(image_data.astype("uint8")).convert("RGB")


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
    def random_valid_ingredient() -> schema.IngredientBase:
        return schema.IngredientBase(
            name="name",
            image_uri=MockImage.random_valid_image_uri(50, 50),
        )

    @staticmethod
    def random_valid_ingredient_data() -> dict[str, Any]:
        return MockIngredient.random_valid_ingredient().model_dump(mode="json")
