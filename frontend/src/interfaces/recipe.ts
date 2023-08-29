import { apiUrl } from '@/env';
import axios from 'axios';
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
    const id = ref();
    const error = ref();

    try {
      id.value = null;
      error.value = null;

      const res = await axios.post(`${apiUrl}/recipes/`, this, {
        headers: {
          authorization: 'bearer create:recipe'
        }
      });

      const result = await res.data;

      id.value = result.id;
    } catch (e) {
      error.value = e;
    }

    return { id, error };
  }
}
