<template>
  <DialogLoading v-model="isLoading" />

  <DialogError v-model="hasError" />

  <DialogSuccess v-model="deleted" />

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
import CardWarning from '@/components/CardWarning.vue';
import DialogError from '@/components/DialogError.vue';
import DialogLoading from '@/components/DialogLoading.vue';
import DialogSuccess from '@/components/DialogSuccess.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeDeletedResponseSchema, type RecipeDeletedResponse } from '@/schema/recipe';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

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
