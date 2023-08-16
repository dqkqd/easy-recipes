from app.models import orm, schema
from app.models.repositories.core import SQLAlchemyRepository


class IngredientRepository(SQLAlchemyRepository):
    def create_ingredient(self, ingredient: schema.IngredientCreate) -> schema.IngredientInDB:
        ingredient_orm = orm.Ingredient(**ingredient.model_dump(mode="json"))
        self.add(ingredient_orm)

        self.commit()  # is there a way we can make it auto_commit before yielding result?
        return schema.IngredientInDB.model_validate(ingredient_orm)
