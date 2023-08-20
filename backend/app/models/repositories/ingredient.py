from app.models.database import orm
from app.models.repositories.core import SQLAlchemyRepository
from app.models.schemas import schema


class IngredientRepository(SQLAlchemyRepository):
    def create_ingredient(
        self,
        ingredient: schema.IngredientCreate,
    ) -> schema.IngredientInDB:
        ingredient_orm = orm.Ingredient(**ingredient.model_dump(mode="json"))
        self.add(ingredient_orm)

        self.commit()  # is there a way we can make it auto_commit before yielding result?
        return schema.IngredientInDB.model_validate(ingredient_orm)

    def get_ingredient(self, id: int) -> schema.IngredientInDB:  # noqa: A002
        ingredient_orm = orm.Ingredient.query.filter_by(id=id).one_or_404()
        return schema.IngredientInDB.model_validate(ingredient_orm)
