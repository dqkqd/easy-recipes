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
    from app.schemas.recipe import RecipeInDBBase


class IngredientIds(BaseSchema):
    ids: list[int] = Field(default_factory=list, alias="ingredients")


class IngredientBaseAbstract(BaseSchema):
    name: Annotated[str, AfterValidator(lambda x: x.strip()), Field(min_length=1)]
    description: str | None = None


class IngredientBase(IngredientBaseAbstract):
    image_uri: HttpUrl | None = None
    likes: int

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl) -> str:
        return str(image_uri)


class IngredientCreate(IngredientBaseAbstract):
    image_uri: HttpUrl | Base64Bytes | None = None
    recipes: list[int] = Field(default_factory=list)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl | Base64Bytes) -> str:
        return str(image_uri)


class IngredientUpdate(IngredientBaseAbstract):
    image_uri: HttpUrl | Base64Bytes | None = None
    recipes: list[int] = Field(default_factory=list)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl | Base64Bytes) -> str:
        return str(image_uri)


class IngredientInDBBase(IDModelMixin, IngredientBase):
    model_config = ConfigDict(from_attributes=True)


class Ingredient(IngredientInDBBase):
    recipes: list[RecipeInDBBase] = Field(default_factory=list)


class AllIngredients(BaseSchema):
    total: int
    ingredients: list[Ingredient]


class PaginatedIngredients(BaseSchema):
    page: int
    ingredients: list[Ingredient]
    total: int
    per_page: int


from app.schemas.recipe import RecipeInDBBase  # noqa: TCH001, F811, E402

Ingredient.model_rebuild()
