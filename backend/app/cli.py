from flask.cli import AppGroup
from pydantic_core import Url

from app.crud import crud_ingredient, crud_recipe
from app.schemas.ingredient import IngredientCreate
from app.schemas.recipe import RecipeCreate

sample_cli = AppGroup("sample")

sample_recipes = {
    "apple_pie": RecipeCreate(
        name="Apple pie",
        description="Very delicous apple pie",
        image_uri=Url("https://images.unsplash.com/photo-1562007908-17c67e878c88"),
    ),
    "orange_juice": RecipeCreate(
        name="Orange juice",
        description="Very delicous orange juice",
        image_uri=Url("https://images.unsplash.com/photo-1613478223719-2ab802602423"),
    ),
    "pumpkin_soup": RecipeCreate(
        name="Pumpkin soup",
        description="Very delicous pumpkin soup",
        image_uri=Url("https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a"),
    ),
}


sample_ingredients = {
    "apple": IngredientCreate(
        name="Apple",
        description="Very delicous apple",
        image_uri=Url("https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6"),
    ),
    "flour": IngredientCreate(
        name="Flour",
        description="Very expensive flour",
        image_uri=Url("https://images.unsplash.com/photo-1627485937980-221c88ac04f9"),
    ),
    "orange": IngredientCreate(
        name="Orange",
        description="Very delicous orange",
        image_uri=Url("https://images.unsplash.com/photo-1582979512210-99b6a53386f9"),
    ),
    "pumpkin": IngredientCreate(
        name="Pumpkin",
        description="Very delicous pumpkin",
        image_uri=Url("https://images.unsplash.com/photo-1570586437263-ab629fccc818"),
    ),
}


@sample_cli.command("add")  # type: ignore  # noqa: PGH003
def add_sample_data() -> None:
    # Apple pie
    apple_pie_recipe = crud_recipe.add(sample_recipes["apple_pie"])
    apple = crud_ingredient.add(sample_ingredients["apple"])
    flour = crud_ingredient.add(sample_ingredients["flour"])
    crud_recipe.update_ingredients(apple_pie_recipe.id, ingredients=[apple, flour])

    # Orange juice
    orange_juice_recipe = crud_recipe.add(sample_recipes["orange_juice"])
    orange = crud_ingredient.add(sample_ingredients["orange"])
    crud_recipe.update_ingredients(orange_juice_recipe.id, ingredients=[orange])

    # Pumpkin soup
    pumpkin_soup_recipe = crud_recipe.add(sample_recipes["pumpkin_soup"])
    pumpkin = crud_ingredient.add(sample_ingredients["pumpkin"])
    crud_recipe.update_ingredients(pumpkin_soup_recipe.id, ingredients=[pumpkin])
