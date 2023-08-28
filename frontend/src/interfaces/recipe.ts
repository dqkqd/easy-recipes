import { apiUrl } from '@/env';
import { type IIngredientBase } from './ingredient';

export interface IRecipeBase {
  name: string;
  description: string | null;
  image_uri: string | null;
}

export interface IRecipeCreate extends IRecipeBase {}

export interface IRecipeWithID extends IRecipeBase {
  id: number;
}

export interface IRecipe extends IRecipeWithID {
  ingredients: Array<IIngredientBase>;
}

export class RecipeBase implements IRecipeBase {
  name: string;
  description: string | null;
  image_uri: string | null;
  constructor(name: string, description: string | null, image_uri: string | null) {
    this.name = name;
    this.description = description;
    this.image_uri = image_uri;
  }
}

export class RecipeCreate extends RecipeBase {
  async insert() {
    try {
      const response = await fetch(`${apiUrl}/recipes`, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          authorization: 'bearer create:recipe'
        },
        body: JSON.stringify(this)
      });

      const result = await response.json();

      if (!result.ok) {
        throw new Error('Invalid Recipe input.');
      }

      return { id: result.id, undefined };
    } catch (e) {
      return { undefined, e };
    }
  }
}
