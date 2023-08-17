from __future__ import annotations

import secrets
from typing import TYPE_CHECKING, Any

from pydantic_core import Url

from app.models.schemas import schema
from app.utils import default_ingredient_image_uri

if TYPE_CHECKING:
    from flask import Flask


def random_str(length: int = 5) -> str:
    return secrets.token_urlsafe(length)


def random_valid_url() -> Url:
    return Url(f"http://{random_str(10)}.com/{random_str(10)}")


def random_invalid_url() -> str:
    return random_str(50)


def ingredient_create_data(app: Flask, name: str | None = None) -> dict[str, Any]:
    ingredient = schema.IngredientCreate(
        name=name if name is not None else random_str(),
        image=default_ingredient_image_uri(app),
    )
    return ingredient.model_dump(mode="json")
