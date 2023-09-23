<template>
  <DialogLoading v-model="isLoading" data-test="recipe-ingredients-dialog-updating" />
  <DialogError
    v-model="hasError"
    title="Can not update recipes's ingredients"
    content="Please try again later..."
    data-test="recipe-ingredients-dialog-updated-error"
  />
  <DialogSuccess
    v-model="updated"
    title="Updated ingredients"
    data-test="recipe-ingredients-dialog-updated-success"
  />

  <VDialog width="800" v-model="dialog">
    <template #activator="{ props }">
      <VBtn
        class="text-body-2"
        color="black"
        text="Add more ingredients"
        data-test="recipe-ingredients-dialog-button"
        v-bind="props"
      />
    </template>
    <RecipeIngredientsDialogSelect
      :selectedIds="selectedIngredientIds"
      @select="selectIngredients"
    />
  </VDialog>
</template>

<script setup lang="ts">
import DialogError from '@/components/DialogError.vue';
import DialogLoading from '@/components/DialogLoading.vue';
import DialogSuccess from '@/components/DialogSuccess.vue';
import RecipeIngredientsDialogSelect from '@/components/RecipeIngredientsDialogSelect.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import type { IngredientBase } from '@/schema/ingredient';
import { RecipeUpdatedResponseSchema, type RecipeUpdatedResponse } from '@/schema/recipe';
import { useAuthStore } from '@/stores/auth';
import { ref } from 'vue';

const props = defineProps<{
  recipeId: number;
  selectedIngredientIds: number[];
}>();

const emit = defineEmits<{
  (e: 'updated', ingredients: IngredientBase[]): void;
}>();

const auth = useAuthStore();

const dialog = ref(false);
const updated = ref(false);

const { result, isLoading, error, execute } = useAxios<RecipeUpdatedResponse>((r) => {
  return RecipeUpdatedResponseSchema.parse(r.data);
});

const { hasError } = useErrorWithTimeout(error, 2000);

async function selectIngredients(selectedIds: number[]) {
  dialog.value = false;

  if ([...props.selectedIngredientIds].sort().toString() === [...selectedIds].sort().toString()) {
    return;
  }

  await execute({
    method: 'patch',
    url: `${apiUrl}/recipes/${props.recipeId}/ingredients/`,
    data: {
      ingredients: selectedIds
    },
    headers: {
      authorization: `Bearer ${auth.token}`
    }
  });

  if (!error.value && result.value) {
    updated.value = true;
    setTimeout(() => {
      updated.value = false;
    }, 1000);

    emit('updated', result.value.ingredients);
  }
}
</script>

<style scoped></style>
