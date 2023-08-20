from app.models.ingredient import Ingredient
from app.repositories.core import SQLAlchemyRepository
from app.schemas.ingredient import IngredientCreate, IngredientInDB


class IngredientRepository(SQLAlchemyRepository):
    def create_ingredient(
        self,
        ingredient_create: IngredientCreate,
    ) -> IngredientInDB:
        ingredient = Ingredient(**ingredient_create.model_dump())
        self.add(ingredient)

        self.commit()  # is there a way we can make it auto_commit before yielding result?
        return IngredientInDB.model_validate(ingredient)

    def get_ingredient(self, id: int) -> IngredientInDB:  # noqa: A002
        ingredient = Ingredient.query.filter_by(id=id).one_or_404()
        return IngredientInDB.model_validate(ingredient)
