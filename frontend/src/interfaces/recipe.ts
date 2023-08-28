import { apiUrl } from '@/env';
import { ref } from 'vue';
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
    const id = ref<number>();
    const error = ref<Error>();

    try {
      error.value = undefined;

      const response = await fetch(`${apiUrl}/recipes`, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          authorization: 'bearer create:recipe'
        },
        body: JSON.stringify(this)
      });

      const result = await response.json();

      id.value = result.id;
    } catch (e) {
      error.value = e as Error;
    }

    return { id, error };
  }
}
