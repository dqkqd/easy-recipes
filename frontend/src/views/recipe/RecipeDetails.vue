<template>
  <div v-if="error" data-test="recipe-details-error">Something wrong ...</div>
  <div v-else-if="result">
    <h1 data-test="recipe-details-name">{{ result.name }}</h1>
    <p data-test="recipe-details-description">{{ result.description }}</p>
    <img v-if="image_uri" :src="image_uri" data-test="recipe-details-valid-image" />
    <img v-else src="/no-image-icon.png" data-test="recipe-details-default-image" />
  </div>
  <div v-else data-test="recipe-details-loading">Loading ...</div>
</template>

<script setup lang="ts">
import { useAxios } from '@/composables';
import { apiUrl, convertFileServerDev } from '@/env';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { computed, onMounted } from 'vue';

const props = defineProps<{ id: number | string }>();

const { result, error, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});

const image_uri = computed(() => {
  if (result.value) {
    return convertFileServerDev(result.value?.image_uri);
  }
  return null;
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
