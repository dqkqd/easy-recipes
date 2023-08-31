<template>
  <div v-if="error" data-test="recipe-details-error">Something wrong ...</div>
  <div v-else-if="result">
    <h1 data-test="recipe-details-name">{{ result.name }}</h1>
    <p data-test="recipe-details-description">{{ result.description }}</p>
    <img v-if="result.image_uri" :src="result.image_uri" data-test="recipe-details-valid-image" />
    <img v-else src="/no-image-icon.png" data-test="recipe-details-default-image" />
  </div>
  <div v-else data-test="recipe-details-loading">Loading ...</div>
</template>

<script setup lang="ts">
import { useAxios } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { onMounted } from 'vue';

const props = defineProps<{ id: number | string }>();

const { result, error, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/${props.id}`
  });
});
</script>

<style scoped></style>
@/schema/recipe
