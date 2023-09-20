import sqlalchemy as sa
from flask_sqlalchemy.pagination import Pagination

from app.crud.base import CRUDBase
from app.database import safe_db
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
)


class CRUDIngredient(
    CRUDBase[
        Ingredient,
        IngredientCreate,
        IngredientUpdate,
    ],
):
    def like(self, id: int, likes: int = 1) -> Ingredient:  # noqa: A002
        ingredient = self.get(id=id)
        ingredient.likes += likes
        with safe_db() as db:
            db.session.commit()
            db.session.refresh(ingredient)
            return ingredient

    def get_pagination_by_recipe_id(
        self,
        recipe_id: int,
        pagination_size: int,
    ) -> Pagination:
        with safe_db() as db:
            return db.paginate(
                sa.select(Ingredient)
                .join(Recipe.ingredients)
                .where(Recipe.id == recipe_id)
                .order_by(Ingredient.id),
                per_page=pagination_size,
                error_out=False,
            )
