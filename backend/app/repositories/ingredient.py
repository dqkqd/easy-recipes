from app.models.ingredient import Ingredient
from app.repositories.core import SQLAlchemyRepository
from app.schemas import schema


class IngredientRepository(SQLAlchemyRepository):
    def create_ingredient(
        self,
        ingredient_create: schema.IngredientCreate,
    ) -> schema.IngredientInDB:
        ingredient = Ingredient(**ingredient_create.model_dump())
        self.add(ingredient)

        self.commit()  # is there a way we can make it auto_commit before yielding result?
        return schema.IngredientInDB.model_validate(ingredient)

    def get_ingredient(self, id: int) -> schema.IngredientInDB:  # noqa: A002
        ingredient = Ingredient.query.filter_by(id=id).one_or_404()
        return schema.IngredientInDB.model_validate(ingredient)
