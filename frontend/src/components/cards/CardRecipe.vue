<template>
  <VHover v-slot="hover">
    <VCard
      @click="toRecipeDetails"
      :elevation="hover && hover.isHovering ? 12 : 2"
      data-test="card-to-recipe-details"
      v-bind="hover && hover.props"
      :class="{ 'recipe-on-hover': hover && hover.isHovering }"
    >
      <VAvatar class="ma-3" :size="256" :rounded="0">
        <VImg :src="imageUri" data-test="card-recipe-image"></VImg>
      </VAvatar>
      <VCardTitle class="text-h5 text-center font-weight-bold" data-test="card-recipe-name">
        {{ recipe.name }}
      </VCardTitle>
    </VCard>
  </VHover>
</template>

<script setup lang="ts">
import { convertFileServerDev } from '@/env';
import type { Recipe } from '@/schema/recipe';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{
  recipe: Recipe;
}>();

const imageUri = computed(() => {
  const image = convertFileServerDev(props.recipe.image_uri);
  return image || '/no-image-icon.png';
});

function toRecipeDetails() {
  router.push({ name: 'RecipeDetails', params: { id: props.recipe.id } });
}
</script>

<style scoped>
.recipe-on-hover {
  color: #40a02b;
}
</style>
