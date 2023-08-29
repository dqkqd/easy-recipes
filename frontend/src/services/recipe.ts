import { useFetchWithParsable } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { RecipeCreate } from '@/interfaces/recipe';
import { RecipeSchema, RecipesResponseSchema } from '@/validator/recipe';
import axios from 'axios';
import { ref } from 'vue';

export function getRecipes() {
  const { data, error } = useFetchWithParsable(RecipesResponseSchema, `${apiUrl}/recipes/`);
  return { recipesResponse: data, error };
}

export function getRecipe(id: number | string) {
  const { data, error } = useFetchWithParsable(RecipeSchema, `${apiUrl}/recipes/${id}`);
  return { recipe: data, error };
}

export async function createRecipe(recipe: RecipeCreate) {
  const id = ref();
  const error = ref<Error>();

  try {
    id.value = null;
    error.value = undefined;

    const res = await axios.post(`${apiUrl}/recipes/`, recipe, {
      headers: {
        authorization: 'bearer create:recipe'
      }
    });

    const result = await res.data;

    id.value = result.id;
  } catch (e) {
    error.value = e as Error;
  }

  return { id, error };
}
