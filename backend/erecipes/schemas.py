from pydantic import BaseModel, ConfigDict, FileUrl, HttpUrl, field_validator

from erecipes.config import BaseConfig


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UniqueNamedModel(Base):
    name: str

    @field_validator("name")
    @classmethod
    def remove_trailing_spaces(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Invalid name.")
        return v


class IngredientBase(UniqueNamedModel):
    image: HttpUrl | FileUrl = BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri()


class Ingredient(IngredientBase):
    id: int  # noqa: A003
