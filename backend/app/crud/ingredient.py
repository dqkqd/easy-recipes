from app.crud.base import CRUDBase
from app.models.ingredient import Ingredient
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
    ...
