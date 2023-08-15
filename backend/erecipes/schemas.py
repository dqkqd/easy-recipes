from pydantic import BaseModel, ConfigDict, FileUrl, HttpUrl

from erecipes.config import BaseConfig


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IngredientBase(Base):
    name: str
    image: HttpUrl | FileUrl = BaseConfig.DEFAULT_INGREDIENT_IMAGE.as_uri()


class Ingredient(IngredientBase):
    id: int  # noqa: A003
