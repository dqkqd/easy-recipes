<template>
  <VHover v-slot="hover">
    <VCard
      :elevation="hover && hover.isHovering ? 12 : 2"
      data-test="card-to-ingredient-details"
      v-bind="hover && hover.props"
      :class="{ 'ingredient-on-hover': hover && hover.isHovering }"
    >
      <VAvatar class="ma-2" :size="100" :rounded="0">
        <VImg :src="imageSrc" @error="onError" data-test="card-ingredient-image"></VImg>
      </VAvatar>
      <VCardTitle class="text-h5 text-center font-weight-bold" data-test="card-ingredient-name">
        {{ ingredient.name }}
      </VCardTitle>
    </VCard>
  </VHover>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import type { Ingredient } from '@/schema/ingredient';

const props = defineProps<{
  ingredient: Ingredient;
}>();

const { imageSrc, onError } = useImage(props.ingredient.image_uri);
</script>

<style scoped>
.ingredient-on-hover {
  color: #40a02b;
}
</style>
