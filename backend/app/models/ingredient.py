from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModelMixin
from app.models.references import recipes_ingredients_association_table

if TYPE_CHECKING:
    from app.models.recipe import Recipe


class Ingredient(BaseModelMixin):
    __tablename__ = "ingredients"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    image_uri: Mapped[str] = mapped_column(nullable=True)

    recipes: Mapped[set[Recipe]] = relationship(
        secondary=recipes_ingredients_association_table,
        back_populates="ingredients",
    )
