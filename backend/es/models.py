from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(Model):
    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()


db = SQLAlchemy(model_class=Base)


class IdModelMixin(db.Model):  # type: ignore
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003


class ImageModelMixin(db.Model):
    __abstract__ = True
    image: Mapped[str]  # @TODO(dqk): add default link


recipes_ingredients_association_table = db.Table(
    "recipes_ingredients",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id"), primary_key=True),
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredients.id"), primary_key=True),
)


class Recipe(IdModelMixin, ImageModelMixin):
    __tablename__ = "recipes"

    ingredients: Mapped[set["Ingredient"]] = relationship(
        secondary=recipes_ingredients_association_table
    )


class Ingredient(IdModelMixin, ImageModelMixin):
    __tablename__ = "ingredients"

    recipes: Mapped[set["Recipe"]] = relationship(secondary=recipes_ingredients_association_table)
