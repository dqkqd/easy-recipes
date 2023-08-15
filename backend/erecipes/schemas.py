from pydantic import BaseModel, ConfigDict, FileUrl, HttpUrl, conlist, field_validator

from erecipes.config import BaseConfig


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NamedModel(Base):
    name: str

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Invalid name.")
        return v


class IngredientBase(NamedModel):
    image: HttpUrl | FileUrl = BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri()


class Ingredient(IngredientBase):
    id: int  # noqa: A003


class RecipeBase(NamedModel):
    image: HttpUrl | FileUrl = BaseConfig.DEFAULT_RECIPE_IMAGE.as_uri()


class RecipeCreate(RecipeBase):
    ingredients: list[int] = conlist(int, min_length=1)


class RecipeInDb(RecipeBase):
    id: int  # noqa: A003
    Ingredient: list[Ingredient] = conlist(Ingredient, min_length=1)
