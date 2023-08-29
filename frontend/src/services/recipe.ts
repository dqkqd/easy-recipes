import { useFetchWithParsable } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { RecipeCreate } from '@/interfaces/recipe';
import { RecipeSchema, RecipesResponseSchema } from '@/validator/recipe';
import axios from 'axios';

export function getRecipes() {
  const { data, error } = useFetchWithParsable(RecipesResponseSchema, `${apiUrl}/recipes/`);
  return { recipesResponse: data, error };
}

export function getRecipe(id: number | string) {
  const { data, error } = useFetchWithParsable(RecipeSchema, `${apiUrl}/recipes/${id}`);
  return { recipe: data, error };
}

export async function createRecipe(
  recipe: RecipeCreate
): Promise<{ id: number | undefined; error: Error | undefined }> {
  try {
    const res = await axios.post(`${apiUrl}/recipes/`, recipe, {
      headers: {
        authorization: 'bearer create:recipe'
      }
    });

    const result = await res.data;

    return { id: result.id, error: undefined };
  } catch (e) {
    return { id: undefined, error: e as Error };
  }
}
