from __future__ import annotations

from typing import TYPE_CHECKING

from app.crud.base import CRUDBase
from app.database import safe_db
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate

if TYPE_CHECKING:
    from app.models.ingredient import Ingredient


class CRUDRecipe(
    CRUDBase[
        Recipe,
        RecipeCreate,
        RecipeUpdate,
    ],
):
    def like(self, id: int, likes: int = 1) -> Recipe:  # noqa: A002
        recipe_db = self.get(id=id)
        recipe_db.likes += likes
        with safe_db() as db:
            db.session.commit()
            db.session.refresh(recipe_db)
            return recipe_db

    def add_ingredients(
        self,
        id: int,  # noqa: A002
        ingredients: list[Ingredient],
    ) -> Recipe:
        recipe_db = self.get(id=id)
        exited_ingredients_ids = {ingredient.id for ingredient in recipe_db.ingredients}
        for ingredient in ingredients:
            if ingredient.id in exited_ingredients_ids:
                continue
            recipe_db.ingredients.append(ingredient)
            exited_ingredients_ids.add(ingredient.id)

        with safe_db() as db:
            db.session.commit()
            db.session.refresh(recipe_db)
            return recipe_db

    def delete_ingredient(
        self,
        id: int,  # noqa: A002
        ingredient: Ingredient,
    ) -> Recipe:
        recipe_db = self.get(id=id)
        recipe_db.ingredients = [
            item for item in recipe_db.ingredients if item.id != ingredient.id
        ]
        with safe_db() as db:
            db.session.commit()
            db.session.refresh(recipe_db)
            return recipe_db
