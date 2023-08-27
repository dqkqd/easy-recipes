import { type IngredientBase } from './ingredient';

export interface RecipeBase {
  name: string;
  description: string | null;
  image_uri: string | null;
}

export interface RecipeCreate extends RecipeBase {}

export interface RecipeWithID extends RecipeBase {
  id: number;
}

export interface Recipe extends RecipeWithID {
  ingredients: Array<IngredientBase>;
}

export class TRecipe implements RecipeBase {
  name: string;
  description: string | null;
  image_uri: string | null;
  constructor(name: string, description: string | null, image_uri: string | null) {
    this.name = name;
    this.description = description;
    this.image_uri = image_uri;
  }
}
