<template>
  <VDialog
    persistent
    width="auto"
    v-model="isLoading"
    data-test="card-recipe-delete-loading-dialog"
  >
    <VProgressCircular color="red" :size="80" indeterminate />
  </VDialog>

  <VDialog width="auto" v-model="hasError" data-test="card-recipe-delete-error-dialog">
    <VAlert prominent :rounded="0" justify="center" type="error" class="px-16 py-5 text-center">
      <VAlertTitle class="text-h5">Can not delete recipe</VAlertTitle>
      <div>Please try again later</div>
    </VAlert>
  </VDialog>

  <VDialog persistent width="auto" v-model="deleted" data-test="card-recipe-delete-deleted-dialog">
    <VAlert prominent :rounded="0" justify="center" type="success" class="px-16 py-5 text-center">
      <VAlertTitle class="text-h5">Recipe deleted</VAlertTitle>
      <div>You will be redirected shortly...</div>
    </VAlert>
  </VDialog>

  <CardWarning
    title="Are you sure you want to delete your recipe?"
    accept-label="Delete"
    cancel-label="Cancel"
    @accept="deleteRecipe"
    @cancel="$emit('cancel')"
    data-test="card-recipe-delete-warning"
  />
</template>

<script setup lang="ts">
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeDeletedResponseSchema, type RecipeDeletedResponse } from '@/schema/recipe';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CardWarning from './CardWarning.vue';

const props = defineProps<{
  id: number;
}>();

const emit = defineEmits<{
  (e: 'cancel'): void;
}>();

const router = useRouter();

const deleted = ref(false);
const hasError = ref(false);

const { result, error, isLoading, execute } = useAxios<RecipeDeletedResponse>((r) => {
  return RecipeDeletedResponseSchema.parse(r.data);
});

async function deleteRecipe() {
  await execute({
    method: 'delete',
    url: `${apiUrl}/recipes/${props.id}`,
    headers: {
      authorization: 'bearer delete:recipe'
    }
  });

  if (!error.value && result.value) {
    deleted.value = true;
    setTimeout(() => {
      router.push({ name: 'RecipeView' });
    }, 1500);
  } else {
    hasError.value = true;
    setTimeout(() => {
      emit('cancel');
    }, 2000);
  }
}
</script>

<style scoped></style>
