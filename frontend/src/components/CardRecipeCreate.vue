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
    </VCard>

    <VDialog
      :width="500"
      v-model="hasError"
      transition="fade-transition"
      data-test="card-recipe-create-error-dialog"
    >
      <VAlert
        color="red-darken-2"
        prominent
        :rounded="0"
        type="error"
        title="Error adding recipe"
      />
    </VDialog>
  </VSheet>
</template>

<script setup lang="ts">
import FormRecipe from '@/components/FormRecipe.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import {
  RecipeCreateSchema,
  RecipeCreatedResponseSchema,
  type RecipeCreatedResponse
} from '@/schema/recipe';
import { useAuthStore } from '@/stores/auth';
import { replaceBase64Prefix } from '@/utils';
import { useRouter } from 'vue-router';

const { result, isLoading, error, execute } = useAxios<RecipeCreatedResponse>(
  (r) => {
    return RecipeCreatedResponseSchema.parse(r.data);
  },
  (data) => {
    const parsedData = RecipeCreateSchema.parse(data);
    parsedData.image_uri = replaceBase64Prefix(parsedData.image_uri);
    return parsedData;
  }
);

const { hasError } = useErrorWithTimeout(error, 2000);

const router = useRouter();

const auth = useAuthStore();

async function createRecipe(name: string, image: string | null, description: string) {
  await execute({
    method: 'post',
    url: `${apiUrl}/recipes/`,
    data: {
      name: name,
      image_uri: image,
      description: description
    },
    headers: {
      authorization: `Bearer ${auth.token}`
    }
  });

  if (!error.value && result.value) {
    router.push({ name: 'RecipeInfo', params: { id: result.value.id } });
  }
}
</script>

<style scoped></style>
