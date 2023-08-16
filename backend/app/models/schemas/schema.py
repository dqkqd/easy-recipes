from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, FileUrl, HttpUrl, field_validator
from pydantic_core import Url

from app.config import BaseConfig
from app.image.b64image import Base64Image
from app.models.schemas.validator import validate_trailing_spaces


class Base(BaseModel):
    pass


class IDModelMixin(Base):
    id: int  # noqa: A003


class IngredientBase(Base):
    name: str
    image: HttpUrl | FileUrl = Url(BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri())

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        return validate_trailing_spaces(v)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientInDB(IDModelMixin, IngredientBase):
    model_config = ConfigDict(from_attributes=True)
    recipes: list[RecipeInDB] = Field(default_factory=list)

    def to_public(self) -> IngredientPublic:
        match self.image:
            case HttpUrl():
                base64_image = Base64Image.from_url(str(self.image))
            case FileUrl():
                base64_image = Base64Image.from_path(Path(self.image))
            case _:
                raise ValueError(self.image)
        return IngredientPublic(
            **self.model_dump(exclude={"image", "recipes"}),
            image=base64_image.data,
            recipes=[recipe.id for recipe in self.recipes],
        )


class IngredientPublic(IDModelMixin):
    name: str
    image: str
    recipes: list[int]


class RecipeBase(Base):
    name: str
    image: HttpUrl | FileUrl = Url(BaseConfig.DEFAULT_RECIPE_IMAGE.as_uri())

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
