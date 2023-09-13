<template>
  <BaseForm
    :loading="loading"
    :name="recipe?.name"
    :description="recipe?.description"
    :image="recipe?.image_uri"
    @submit="submit"
  />
</template>

<script setup lang="ts">
import BaseForm from '@/components/BaseForm.vue';
import type { Recipe } from '@/schema/recipe';

withDefaults(
  defineProps<{
    loading?: boolean;
    recipe?: Recipe;
  }>(),
  {
    loading: false
  }
);

const emit = defineEmits<{
  (e: 'submit', name: string, image: string | null, description: string): void;
}>();

function submit(name: string, image: string | null, description: string) {
  emit('submit', name, image, description);
}
</script>

<style scoped></style>
