from sqlalchemy.orm import Mapped, mapped_column, relationship

from erecipes.models import db


class BaseModelMixin(db.Model):  # type: ignore
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(unique=True)
    image: Mapped[str]  # @TODO(dqk): add default link

    @property
    def unique_name(self) -> str:
        count = self.query.filter_by(name=self.name).count()
        return self.name if count == 0 else f"{self.name}_{count}"

    def insert(self) -> None:
        """Insert with unique name"""
        try:
            super().insert()
        except Exception:
            db.session.rollback()
            self.name = self.unique_name
            super().insert()


recipes_ingredients_association_table = db.Table(
    "recipes_ingredients",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id"), primary_key=True),
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredients.id"), primary_key=True),
)


class Recipe(BaseModelMixin):
    __tablename__ = "recipes"

    ingredients: Mapped[set["Ingredient"]] = relationship(
        secondary=recipes_ingredients_association_table, back_populates="recipes"
    )


class Ingredient(BaseModelMixin):
    __tablename__ = "ingredients"

    recipes: Mapped[set["Recipe"]] = relationship(
        secondary=recipes_ingredients_association_table,
        back_populates="ingredients",
    )
