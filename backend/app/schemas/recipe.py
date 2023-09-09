from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

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

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl) -> str:
        return str(image_uri)


class RecipeCreate(RecipeBaseAbstract):
    image_uri: HttpUrl | Base64Bytes | None = None
    ingredients: set[int] = Field(default_factory=set)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl | Base64Bytes) -> str:
        return str(image_uri)


class RecipeUpdate(RecipeBaseAbstract):
    image_uri: HttpUrl | Base64Bytes | None = None
    ingredients: set[int] = Field(default_factory=set)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl | Base64Bytes) -> str:
        return str(image_uri)


class RecipeInDBBase(IDModelMixin, RecipeBase):
    model_config = ConfigDict(from_attributes=True)


class Recipe(RecipeInDBBase):
    ingredients: set[IngredientInDBBase] = Field(default_factory=set)


from app.schemas.ingredient import IngredientInDBBase  # noqa: TCH001, E402, F811

Recipe.model_rebuild()
