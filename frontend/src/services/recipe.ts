import { useFetchWithParsable } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { TRecipe } from '@/interfaces/recipe';
import { RecipesResponseSchema } from '@/validator/recipe';
import { ref } from 'vue';

export function getRecipes() {
  const { data, error } = useFetchWithParsable(RecipesResponseSchema, `${apiUrl}/recipes`);
  return { recipesResponse: data, error };
}

export function createRecipe() {
  const recipeCreate = ref<TRecipe>(new TRecipe('', null, null));
  const error = ref<Error>();
  const create = async () => {
    try {
      error.value = undefined;

      const response = await fetch(`${apiUrl}/recipes`, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          authorization: 'bearer create:recipe'
        },
        body: JSON.stringify(recipeCreate.value)
      });
      const result = await response.json();
      console.log(result.message);
    } catch (e) {
      error.value = e as Error;
    }
  };
  return { recipeCreate, create };
}
