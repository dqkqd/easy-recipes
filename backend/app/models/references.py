from __future__ import annotations

from app.database import db

recipes_ingredients_association_table = db.Table(
    "recipes_ingredients",
    db.Column("recipe_id", db.Integer, db.ForeignKey("recipes.id"), primary_key=True),
    db.Column(
        "ingredient_id",
        db.Integer,
        db.ForeignKey("ingredients.id"),
        primary_key=True,
    ),
)
