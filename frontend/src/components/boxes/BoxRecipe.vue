<template>
  <div class="box" @click="toRecipeDetails">
    <div data-test="box-recipe-name">{{ props.recipe.name }}</div>
    <div v-if="props.recipe.description" data-test="box-recipe-description">
      {{ props.recipe.description }}
    </div>
    <img
      v-if="props.recipe.image_uri"
      class="recipe-image"
      :src="image_uri"
      data-test="box-recipe-valid-image"
    />
    <img
      v-else
      class="recipe-image"
      src="/no-image-icon.png"
      data-test="box-recipe-default-image"
    />
  </div>
</template>

<script setup lang="ts">
import { convertFileServerDev } from '@/env';
import type { Recipe } from '@/interfaces/recipe';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{
  recipe: Recipe;
}>();

const image_uri = computed(() => {
  return props.recipe.image_uri ? convertFileServerDev(props.recipe.image_uri) : undefined;
});

function toRecipeDetails() {
  router.push({ name: 'RecipeDetails', params: { id: props.recipe.id } });
}
</script>

<style scoped>
.title {
  font-size: 1.5rem;
  margin: 5px;
  font-weight: bold;
  text-align: center;
}

.box {
  width: 200px;
  height: 200px;
  border: 1px solid;
  transition: transform 0.2s;
  margin: 5px;
}

.bigger-box {
  width: 500px;
  height: 500px;
}

.box:hover {
  box-shadow: 5px 5px 5px #eee;
  transform: scale(1.2);
}

.recipe-image {
  width: 150px;
  height: 150px;
  margin: auto;
  display: block;
}
</style>
