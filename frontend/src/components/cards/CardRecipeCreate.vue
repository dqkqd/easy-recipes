<template>
  <VSheet :width="800">
    <VCard class="px-5 pb-8">
      <VCardTitle
        class="text-center my-8 py-1 font-weight-black text-h4"
        data-test="card-recipe-create-title"
        >Add new recipe</VCardTitle
      >

      <FormRecipe
        :loading="isLoading"
        @submit="createRecipe"
        data-test="card-recipe-create-form-recipe"
      />

      <VDialog v-model="hasError" transition="fade-transition" data-test="card-recipe-error-dialog">
        <VAlert prominent :rounded="0" type="error" title="Error adding recipe" />
      </VDialog>
    </VCard>
  </VSheet>
</template>

<script setup lang="ts">
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import {
  RecipeCreateSchema,
  RecipeCreatedResponseSchema,
  type RecipeCreatedResponse
} from '@/schema/recipe';
import { useRouter } from 'vue-router';
import FormRecipe from '../forms/FormRecipe.vue';

const router = useRouter();
const { result, isLoading, error, execute } = useAxios<RecipeCreatedResponse>(
  (r) => {
    return RecipeCreatedResponseSchema.parse(r.data);
  },
  (data) => {
    return RecipeCreateSchema.parse(data);
  }
);

const { hasError } = useErrorWithTimeout(error, 2000);

async function createRecipe(name: string, imageUri: string, description: string) {
  await execute({
    method: 'post',
    url: `${apiUrl}/recipes/`,
    data: {
      name: name,
      image_uri: imageUri,
      description: description
    },
    headers: {
      authorization: 'bearer create:recipe'
    }
  });

  if (!error.value && result.value) {
    router.push({ name: 'RecipeInfo', params: { id: result.value.id } });
  }
}
</script>

<style scoped></style>
