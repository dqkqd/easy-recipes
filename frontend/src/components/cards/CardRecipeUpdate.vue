<template>
  <VSheet :width="800">
    <VCard class="px-5 pb-8">
      <VCardTitle
        class="text-center my-8 py-1 font-weight-black text-h4"
        data-test="card-recipe-update-title"
        >Update your recipe</VCardTitle
      >

      <FormRecipe
        :loading="isLoading"
        :recipe="recipe"
        @submit="updateRecipe"
        @cancel="$emit('cancel')"
        data-test="card-recipe-update-form-recipe"
      />

      <VDialog
        v-model="hasError"
        transition="fade-transition"
        data-test="card-recipe-update-error-dialog"
      >
        <VAlert prominent :rounded="0" type="error" title="Error updating recipe" />
      </VDialog>
    </VCard>
  </VSheet>
</template>

<script setup lang="ts">
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl, convertFileServerDev } from '@/env';
import {
  RecipeUpdateSchema,
  RecipeUpdatedResponseSchema,
  type Recipe,
  type RecipeUpdatedResponse
} from '@/schema/recipe';
import { replaceBase64Prefix } from '@/utils';
import FormRecipe from '../forms/FormRecipe.vue';

const props = defineProps<{
  recipe: Recipe;
}>();

const emit = defineEmits<{
  (e: 'updated', name: string, image_uri: string | null, description: string): void;
  (e: 'cancel'): void;
}>();

const { result, isLoading, error, execute } = useAxios<RecipeUpdatedResponse>(
  (r) => {
    return RecipeUpdatedResponseSchema.parse(r.data);
  },
  (data) => {
    const parsedData = RecipeUpdateSchema.parse(data);
    parsedData.image_uri = replaceBase64Prefix(parsedData.image_uri);
    return parsedData;
  }
);

const { hasError } = useErrorWithTimeout(error, 2000);

async function updateRecipe(name: string, image: string | null, description: string) {
  if (
    props.recipe.name !== name ||
    convertFileServerDev(props.recipe.image_uri) !== image ||
    props.recipe.description !== description
  ) {
    await execute({
      method: 'patch',
      url: `${apiUrl}/recipes/${props.recipe.id}`,
      data: {
        name: name,
        image_uri: image,
        description: description
      },
      headers: {
        authorization: 'bearer update:recipe'
      }
    });
  }

  if (!error.value && result.value) {
    emit('updated', result.value.name, result.value.image_uri, result.value.description ?? '');
  }
}
</script>

<style scoped></style>
