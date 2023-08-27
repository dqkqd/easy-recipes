import { type IngredientBase } from './ingredient';

export interface RecipeBase {
  id: number;
  name: string;
  description: string | null;
  image_uri: string | null;
}

export interface Recipe extends RecipeBase {
  ingredients: Array<IngredientBase>;
}
