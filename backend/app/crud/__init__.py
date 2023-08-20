from app.crud.ingredient import CRUDIngredient
from app.crud.recipe import CRUDRecipe
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe

crud_ingredient = CRUDIngredient(Ingredient)
crud_recipe = CRUDRecipe(Recipe)
