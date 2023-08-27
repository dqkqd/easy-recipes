import { useFetchWithParsable } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { RecipeCreate } from '@/interfaces/recipe';
import { RecipeSchema, RecipesResponseSchema } from '@/validator/recipe';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export function getRecipes() {
  const { data, error } = useFetchWithParsable(RecipesResponseSchema, `${apiUrl}/recipes`);
  return { recipesResponse: data, error };
}

export function getRecipe(id: any) {
  const parsedId = parseInt(id);
  if (isNaN(parsedId)) {
    return { recipe: ref(null), error: ref(new TypeError(`Invalid route with recipe id = ${id}`)) };
  }
  const { data, error } = useFetchWithParsable(RecipeSchema, `${apiUrl}/recipes/${parsedId}`);
  return { recipe: data, error };
}

export function createRecipe() {
  const recipeCreate = ref<RecipeCreate>(new RecipeCreate('', null, null));
  const error = ref<Error>();

  const router = useRouter();

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
      router.push(`/recipes/${result.id}`);
    } catch (e) {
      error.value = e as Error;
    }
  };
  return { recipeCreate, create };
}
