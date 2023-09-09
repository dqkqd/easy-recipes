<template>
  <VRow justify="center">
    <VDialog v-model="dialog" width="auto">
      <template v-slot:activator="{ props }">
        <VBtn icon="mdi-pencil" v-bind="props" data-test="recipe-details-edit-button" />
      </template>

      <VSheet :width="800">
        <VCard class="px-5 pb-8">
          <VCardTitle
            class="text-center my-8 py-1 font-weight-black text-h4"
            data-test="card-recipe-edit-title"
            >Edit your recipe</VCardTitle
          >

          <FormRecipe
            :loading="isLoading"
            :recipe-name="recipe.name"
            :recipe-image-uri="recipe.image_uri"
            :recipe-description="recipe.description"
            @submit="editRecipe"
            @cancel="dialog = false"
            data-test="card-recipe-edit-form-recipe"
          />

          <VDialog
            v-model="hasError"
            transition="fade-transition"
            data-test="card-recipe-edit-error-dialog"
          >
            <VAlert prominent :rounded="0" type="error" title="Error editing recipe" />
          </VDialog>
        </VCard>
      </VSheet>
    </VDialog>
  </VRow>
</template>

<script setup lang="ts">
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import {
  RecipeUpdateSchema,
  RecipeUpdatedResponseSchema,
  type Recipe,
  type RecipeUpdatedResponse
} from '@/schema/recipe';
import { ref } from 'vue';
import FormRecipe from '../forms/FormRecipe.vue';

const props = defineProps<{
  recipe: Recipe;
}>();

const emit = defineEmits<{
  (e: 'updated'): void;
}>();

const dialog = ref(false);

const { result, isLoading, error, execute } = useAxios<RecipeUpdatedResponse>(
  (r) => {
    return RecipeUpdatedResponseSchema.parse(r.data);
  },
  (data) => {
    return RecipeUpdateSchema.parse(data);
  }
);

const { hasError } = useErrorWithTimeout(error, 2000);

async function editRecipe(name: string, imageUri: string, description: string) {
  await execute({
    method: 'post',
    url: `${apiUrl}/recipes/${props.recipe.id}`,
    data: {
      name: name,
      image_uri: imageUri,
      description: description
    },
    headers: {
      authorization: 'bearer update:recipe'
    }
  });

  if (!error.value && result.value) {
    emit('updated');
  }
}
</script>

<style scoped></style>
