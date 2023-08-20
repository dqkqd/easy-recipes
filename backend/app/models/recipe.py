from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.models.base import BaseModelMixin, ToSchemaModelMixin
from app.models.references import recipes_ingredients_association_table

if TYPE_CHECKING:
    from app.models.ingredient import Ingredient


class Recipe(BaseModelMixin, ToSchemaModelMixin):
    __tablename__ = "recipes"

    ingredients: Mapped[set[Ingredient]] = relationship(
        secondary=recipes_ingredients_association_table,
        back_populates="recipes",
    )
