import { type IRecipeBase } from './recipe';

export interface IIngredientBase {
  name: string;
  description: string | null;
  image_uri: string | null;
}

export interface IIngredientWithID extends IRecipeBase {
  id: number;
}

export interface IIngredient extends IIngredientBase {
  recipes: Array<IRecipeBase>;
}

export interface IIngredient extends IIngredientWithID {
  ingredients: Array<IRecipeBase>;
}

export class IngredientBase implements IIngredientBase {
  name: string;
  description: string | null;
  image_uri: string | null;
  constructor(name: string, description: string | null, image_uri: string | null) {
    this.name = name;
    this.description = description;
    this.image_uri = image_uri;
  }
}

export class IngredientCreate extends IngredientBase {}
