<template>
  <div v-if="error">Something wrong.</div>
  <div v-else-if="recipe">
    <h1>{{ recipe.name }}</h1>
    <p>{{ recipe.description }}</p>
    <img v-if="image_uri" :src="image_uri" />
  </div>
  <div v-else>Loading...</div>
</template>

<script setup lang="ts">
import { convertFileServerDev } from '@/env';
import { getRecipe } from '@/services/recipe';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const { recipe, error } = getRecipe(route.params.id);
const image_uri = computed(() => {
  if (recipe.value && recipe.value.image_uri) {
    return convertFileServerDev(recipe.value.image_uri);
  }
  return null;
});
</script>

<style scoped></style>
