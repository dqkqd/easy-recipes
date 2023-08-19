from __future__ import annotations

import secrets
from typing import Any

import numpy as np
from PIL import Image
from pydantic_core import Url

from app.models.schemas import schema


def random_str(length: int = 5) -> str:
    return secrets.token_urlsafe(length)


def random_valid_url() -> Url:
    return Url(f"http://{random_str(10)}.com/{random_str(10)}")


def ingredient_create_data(name: str | None = None) -> dict[str, Any]:
    ingredient = schema.IngredientCreate(
        name=name if name is not None else random_str(),
        image=random_valid_url(),
    )
    return ingredient.model_dump(mode="json")


def random_image(w: int, h: int) -> Image.Image:
    rng = np.random.default_rng(seed=42)
    image_data = rng.random((w, h, 3)) * 255
    return Image.fromarray(image_data.astype("uint8")).convert("RGB")
