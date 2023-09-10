<template>
  <VHover v-slot="hover">
    <VCard
      @click="router.push({ name: 'RecipeInfo', params: { id: recipe.id } })"
      :elevation="hover && hover.isHovering ? 12 : 2"
      data-test="card-to-recipe-details"
      v-bind="hover && hover.props"
      :class="{ 'recipe-on-hover': hover && hover.isHovering }"
    >
      <VAvatar class="ma-3" :size="256" :rounded="0">
        <VImg :src="imageSrc" @error="onError" data-test="card-recipe-image"></VImg>
      </VAvatar>
      <VCardTitle class="text-h5 text-center font-weight-bold" data-test="card-recipe-name">
        {{ recipe.name }}
      </VCardTitle>
    </VCard>
  </VHover>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import type { Recipe } from '@/schema/recipe';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{
  recipe: Recipe;
}>();

const { imageSrc, onError } = useImage(props.recipe.image_uri);
</script>

<style scoped>
.recipe-on-hover {
  color: #40a02b;
}
</style>
