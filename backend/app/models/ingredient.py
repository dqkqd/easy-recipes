from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.models.base import BaseModelMixin, ToSchemaModelMixin
from app.models.references import recipes_ingredients_association_table

if TYPE_CHECKING:
    from app.models.recipe import Recipe


class Ingredient(BaseModelMixin, ToSchemaModelMixin):
    __tablename__ = "ingredients"

    recipes: Mapped[set[Recipe]] = relationship(
        secondary=recipes_ingredients_association_table,
        back_populates="ingredients",
    )
