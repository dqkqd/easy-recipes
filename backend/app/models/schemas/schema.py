from __future__ import annotations

from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
)

from app.models.schemas.validators import validate_trailing_spaces


class Base(BaseModel):
    pass


class IDModelMixin(Base):
    id: int  # noqa: A003


class IngredientBase(Base):
    name: str
    image_uri: HttpUrl | None = None

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        return validate_trailing_spaces(v)


class IngredientFromUser(Base):
    name: Annotated[str, AfterValidator(lambda x: x.strip())]
    image_uri: HttpUrl | None = None
    recipes: list[int] = Field(default_factory=list)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientInDB(IDModelMixin, IngredientBase):
    model_config = ConfigDict(from_attributes=True)
    recipes: list[RecipeInDB] = Field(default_factory=list)

    def to_public(self) -> IngredientPublic:
        return IngredientPublic(
            **self.model_dump(exclude={"recipes"}),
            recipes=[recipe.id for recipe in self.recipes],
        )


class IngredientPublic(IDModelMixin):
    name: str
    image_uri: HttpUrl | None
    recipes: list[int] = Field(default_factory=list)


class RecipeBase(Base):
    name: str
    image_uri: HttpUrl | None

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        return validate_trailing_spaces(v)


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeInDB(IDModelMixin, RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    ingredients: list[IngredientInDB] = Field(default_factory=list)
