from __future__ import annotations

from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_serializer,
)


class Base(BaseModel):
    pass


class IDModelMixin(Base):
    id: int  # noqa: A003


class IngredientBase(Base):
    name: Annotated[str, AfterValidator(lambda x: x.strip()), Field(min_length=1)]
    image_uri: HttpUrl | None = None
    recipes: set[int] = Field(default_factory=set)

    @field_serializer("image_uri", when_used="unless-none")
    def serialize_image_uri(self, image_uri: HttpUrl) -> str:
        return str(image_uri)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientInDB(IDModelMixin, IngredientBase):
    model_config = ConfigDict(from_attributes=True)
    recipes: set[RecipeInDB] = Field(default_factory=set)

    def to_public(self) -> IngredientPublic:
        return IngredientPublic(
            **self.model_dump(exclude={"recipes"}),
            recipes=[recipe.id for recipe in self.recipes],
        )


class IngredientPublic(IDModelMixin, IngredientBase):
    pass


class RecipeBase(Base):
    name: Annotated[str, AfterValidator(lambda x: x.strip()), Field(min_length=1)]
    image_uri: HttpUrl | None = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeInDB(IDModelMixin, RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    ingredients: set[IngredientInDB] = Field(default_factory=set)
