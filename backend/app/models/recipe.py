from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModelMixin
from app.models.references import recipes_ingredients_association_table

if TYPE_CHECKING:
    from app.models.ingredient import Ingredient


class Recipe(BaseModelMixin):
    __tablename__ = "recipes"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    image_uri: Mapped[str] = mapped_column(nullable=True)
    likes: Mapped[int] = mapped_column(default=0)

    ingredients: Mapped[set[Ingredient]] = relationship(
        secondary=recipes_ingredients_association_table,
        back_populates="recipes",
    )
