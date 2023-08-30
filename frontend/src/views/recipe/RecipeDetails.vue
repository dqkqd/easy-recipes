<template>
  <div v-if="error">Something wrong.</div>
  <div v-else-if="result">
    <h1>{{ result.name }}</h1>
    <p>{{ result.description }}</p>
    <img v-if="image_uri" :src="image_uri" />
    <img v-else src="/no-image-icon.png" />
  </div>
  <div v-else>Loading...</div>
</template>

<script setup lang="ts">
import { useAxios } from '@/composables/fetch';
import { apiUrl, convertFileServerDev } from '@/env';
import type { Recipe } from '@/interfaces/recipe';
import { RecipeSchema } from '@/validator/recipe';
import { computed, onMounted } from 'vue';

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

const image_uri = computed(() => {
  if (result.value && result.value.image_uri) {
    return convertFileServerDev(result.value.image_uri);
  }
  return null;
});
</script>

<style scoped></style>
