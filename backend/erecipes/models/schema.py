from pydantic import BaseModel, ConfigDict, Field, FileUrl, HttpUrl, field_validator

from erecipes.config import BaseConfig


class Base(BaseModel):
    pass


class IDModelMixin(Base):
    id: int  # noqa: A003


class IngredientBase(Base):
    name: str
    image: HttpUrl | FileUrl = BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri()

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Invalid name.")
        return v


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientInDB(IDModelMixin, IngredientBase):
    model_config = ConfigDict(from_attributes=True)
    recipes: list["RecipeInDB"] = Field(default_factory=list)


class RecipeBase(Base):
    name: str
    image: HttpUrl | FileUrl = BaseConfig.DEFAULT_RECIPE_IMAGE.as_uri()

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Invalid name.")
        return v


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeInDB(IDModelMixin, RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    ingredients: list[IngredientInDB] = Field(default_factory=list)
