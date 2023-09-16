from __future__ import annotations

import io
import secrets
import uuid
from typing import TYPE_CHECKING, Any

import numpy as np
from PIL import Image

from app import auth
from app.file_server.image import ImageOnServer
from app.schemas.ingredient import IngredientCreate
from app.schemas.recipe import RecipeCreate
from tests.utils import (
    get_manager_token,
    get_menu_manager_token,
    should_use_real_auth_test,
)

if TYPE_CHECKING:
    from pydantic_core import Url


def random_id() -> str:
    return uuid.uuid4().hex


def random_str(size: int = 256) -> str:
    return secrets.token_urlsafe(size)


class MockImage:
    @staticmethod
    def random(w: int, h: int) -> Image.Image:
        rng = np.random.default_rng(seed=42)
        image_data = rng.random((w, h, 3)) * 255
        return Image.fromarray(image_data.astype("uint8")).convert("RGB")

    @staticmethod
    def random_bytes(w: int, h: int) -> io.BytesIO:
        image = MockImage.random(w, h)
        stream = io.BytesIO()
        image.save(stream, format="PNG")
        return stream

    @staticmethod
    def random_uri(w: int, h: int) -> Url:
        with ImageOnServer.from_source(
            MockImage.random_bytes(w, h),
        ) as image_on_server:
            return image_on_server.uri


class MockIngredient:
    @staticmethod
    def random() -> IngredientCreate:
        return IngredientCreate(
            name=random_id(),
            description=random_str(256),
            image_uri=MockImage.random_uri(50, 50),
        )

    @staticmethod
    def random_data() -> dict[str, Any]:
        return MockIngredient.random().model_dump(mode="json")


class MockRecipe:
    @staticmethod
    def random() -> RecipeCreate:
        return RecipeCreate(
            name=random_id(),
            description=random_str(256),
            image_uri=MockImage.random_uri(50, 50),
        )

    @staticmethod
    def random_data() -> dict[str, Any]:
        return MockRecipe.random().model_dump(mode="json")


class MockAuth:
    @staticmethod
    def header(permission: str) -> dict[str, str]:
        token = permission
        if should_use_real_auth_test():
            menu_manager_token = get_menu_manager_token()
            manager_token = get_manager_token()
            if menu_manager_token is None or manager_token is None:
                raise RuntimeError("Something wrong with authentication tokens")

            match permission:
                case (
                    auth.CREATE_INGREDIENT_PERMISSION
                    | auth.UPDATE_INGREDIENT_PERMISSION
                    | auth.CREATE_RECIPE_PERMISSION
                    | auth.UPDATE_RECIPE_PERMISSION
                ):
                    token = menu_manager_token
                case auth.DELETE_INGREDIENT_PERMISSION | auth.DELETE_RECIPE_PERMISSION:
                    token = manager_token
                case _:
                    pass

        return {"Authorization": f"Bearer {token}"}
