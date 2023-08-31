import { useFetchWithParsable } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { RecipesResponseSchema } from '@/schema/recipe';

export function getRecipes() {
  const { data, error } = useFetchWithParsable(RecipesResponseSchema, `${apiUrl}/recipes/`);
  return { recipesResponse: data, error };
}
