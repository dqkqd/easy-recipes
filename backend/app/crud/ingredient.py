from app.crud.base import CRUDBase
from app.models.ingredient import Ingredient
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientInDB,
    IngredientPublic,
    IngredientUpdate,
)


class CRUDIngredient(
    CRUDBase[
        Ingredient,
        IngredientCreate,
        IngredientUpdate,
        IngredientInDB,
        IngredientPublic,
    ],
):
    def create(
        self,
        ingredient_create: IngredientCreate,
    ) -> IngredientInDB:
        ingredient = Ingredient(**ingredient_create.model_dump())
        self.add(ingredient)

        self.commit()  # is there a way we can make it auto_commit before yielding result?
        return IngredientInDB.model_validate(ingredient)

    def get_by_id(self, id: int) -> IngredientInDB:  # noqa: A002
        ingredient = Ingredient.query.filter_by(id=id).one_or_404()
        return IngredientInDB.model_validate(ingredient)
