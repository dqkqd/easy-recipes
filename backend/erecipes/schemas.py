from pydantic import BaseModel, ConfigDict, FileUrl, HttpUrl


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IngredientBase(Base):
    name: str
    image: HttpUrl | FileUrl


class Ingredient(IngredientBase):
    id: int  # noqa: A003
