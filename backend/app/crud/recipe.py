from app.crud.base import CRUDBase
from app.database import safe_db
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate


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
