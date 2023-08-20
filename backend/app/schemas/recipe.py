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
    from app.schemas.ingredient import IngredientInDB


class RecipeBase(BaseSchema):
    name: Annotated[str, AfterValidator(lambda x: x.strip()), Field(min_length=1)]
    description: str | None = None
    image_uri: HttpUrl | None = None

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl) -> str:
        return str(image_uri)


class RecipeCreate(RecipeBase):
    recipes: set[int] = Field(default_factory=set)


class RecipeUpdate(RecipeBase):
    pass


class RecipeInDB(IDModelMixin, RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    ingredients: set[IngredientInDB] = Field(default_factory=set)

    def to_public(self) -> RecipePublic:
        return RecipePublic(
            **self.model_dump(exclude={"ingredients"}),
            ingredients={ingredient.id for ingredient in self.ingredients},
        )


class RecipePublic(IDModelMixin, RecipeBase):
    ingredients: set[int] = Field(default_factory=set)


# https://stackoverflow.com/questions/63420889/fastapi-pydantic-circular-references-in-separate-files
from app.schemas.ingredient import IngredientInDB  # noqa: E402, TCH001, F811

RecipeInDB.model_rebuild()
