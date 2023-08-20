from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import (
    AfterValidator,
    ConfigDict,
    Field,
    HttpUrl,
    field_serializer,
)

from app.schemas.base import BaseSchema, IDModelMixin

if TYPE_CHECKING:
    from app.schemas.recipe import RecipeInDB


class IngredientBase(BaseSchema):
    name: Annotated[str, AfterValidator(lambda x: x.strip()), Field(min_length=1)]
    description: str | None = None
    image_uri: HttpUrl | None = None

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl) -> str:
        return str(image_uri)


class IngredientCreate(IngredientBase):
    recipes: set[int] = Field(default_factory=set)


class IngredientUpdate(IngredientBase):
    pass


class IngredientInDB(IDModelMixin, IngredientBase):
    model_config = ConfigDict(from_attributes=True)

    recipes: set[RecipeInDB] = Field(default_factory=set)

    def to_public(self) -> IngredientPublic:
        return IngredientPublic(
            **self.model_dump(exclude={"recipes"}),
            recipes={recipe.id for recipe in self.recipes},
        )


class IngredientPublic(IDModelMixin, IngredientBase):
    recipes: set[int] = Field(default_factory=set)


# https://stackoverflow.com/questions/63420889/fastapi-pydantic-circular-references-in-separate-files
from app.schemas.recipe import RecipeInDB  # noqa: E402, F811, TCH001

IngredientInDB.model_rebuild()
