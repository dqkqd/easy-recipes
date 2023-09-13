<template>
  <BaseForm
    :loading="loading"
    :name="ingredient?.name"
    :description="ingredient?.description"
    :image="ingredient?.image_uri"
    @submit="submit"
    data-test="form-ingredient"
  />
</template>

<script setup lang="ts">
import BaseForm from '@/components/BaseForm.vue';
import type { Ingredient } from '@/schema/ingredient';

withDefaults(
  defineProps<{
    loading?: boolean;
    ingredient?: Ingredient;
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
