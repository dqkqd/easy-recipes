import { type IRecipeBase } from './recipe';

export interface IIngredientBase {
  id: number;
  name: string;
  description: string | null;
  image_uri: string | null;
}

export interface IIngredient extends IIngredientBase {
  recipes: Array<IRecipeBase>;
}
