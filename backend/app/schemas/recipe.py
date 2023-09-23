from __future__ import annotations

import socket
from typing import TYPE_CHECKING, Annotated

from flask import current_app
from pydantic import (
    AfterValidator,
    Base64Bytes,
    ConfigDict,
    Field,
    HttpUrl,
    field_serializer,
)

from app.schemas.base import BaseSchema, IDModelMixin

if TYPE_CHECKING:
    from app.schemas.ingredient import IngredientInDBBase


class RecipeBaseAbstract(BaseSchema):
    name: Annotated[str, AfterValidator(lambda x: x.strip()), Field(min_length=1)]
    description: str | None = None


class RecipeBase(RecipeBaseAbstract):
    image_uri: HttpUrl | None = None
    likes: int

    @field_serializer("image_uri", when_used="json-unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl) -> str:
        file_server_host = current_app.config["FILE_SERVER_HOST"]
        if image_uri.host == file_server_host:
            image_uri = image_uri.build(
                scheme=image_uri.scheme,
                username=image_uri.username,
                password=image_uri.password,
                host=socket.gethostbyname(file_server_host),
                port=image_uri.port,
                path=image_uri.path,
                query=image_uri.query,
                fragment=image_uri.fragment,
            )
        return str(image_uri)


class RecipeCreate(RecipeBaseAbstract):
    image_uri: HttpUrl | Base64Bytes | None = None
    ingredients: list[int] = Field(default_factory=list)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl | Base64Bytes) -> str:
        return str(image_uri)


class RecipeUpdate(RecipeBaseAbstract):
    image_uri: HttpUrl | Base64Bytes | None = None
    ingredients: list[int] = Field(default_factory=list)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl | Base64Bytes) -> str:
        return str(image_uri)


class RecipeInDBBase(IDModelMixin, RecipeBase):
    model_config = ConfigDict(from_attributes=True)


class Recipe(RecipeInDBBase):
    ingredients: list[IngredientInDBBase] = Field(default_factory=list)


class AllRecipes(BaseSchema):
    total: int
    recipes: list[Recipe]


class PaginatedRecipes(BaseSchema):
    page: int
    recipes: list[Recipe]
    total: int
    per_page: int


from app.schemas.ingredient import IngredientInDBBase  # noqa: TCH001, E402, F811

Recipe.model_rebuild()
