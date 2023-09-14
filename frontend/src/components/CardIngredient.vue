<template>
  <VHover v-slot="hover">
    <VDialog v-model="dialog" :width="500">
      <IngredientDetails :ingredient="ingredient" />
    </VDialog>

    <VCard
      :width="130"
      @click="dialog = true"
      :elevation="hover && hover.isHovering ? 12 : 2"
      data-test="card-to-ingredient-details"
      v-bind="hover && hover.props"
      :class="{ 'ingredient-on-hover': hover && hover.isHovering }"
    >
      <VImg
        :src="imageSrc"
        @error="onError"
        lazy-src="/ingredient-cover.jpg"
        :height="100"
        :width="130"
        cover
        data-test="card-ingredient-image"
      />
      <VCardTitle class="text-center font-weight-bold" data-test="card-ingredient-name">
        {{ ingredientName }}
      </VCardTitle>
    </VCard>
  </VHover>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import type { Ingredient } from '@/schema/ingredient';
import { stripText } from '@/utils';
import { computed, ref } from 'vue';
import IngredientDetails from './IngredientDetails.vue';

const props = defineProps<{
  ingredient: Ingredient;
}>();

const dialog = ref(false);

const ingredientName = computed(() => stripText(props.ingredient.name, 10));

const { imageSrc, onError } = useImage(props.ingredient.image_uri);
</script>

<style scoped>
.ingredient-on-hover {
  color: #40a02b;
}
</style>
