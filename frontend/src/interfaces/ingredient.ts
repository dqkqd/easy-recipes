import { type RecipeBase } from './recipe';

export interface IngredientBase {
  id: number;
  name: string;
  description: string | null;
  image_uri: string | null;
}

export interface Ingredient extends IngredientBase {
  recipes: Array<RecipeBase>;
}
