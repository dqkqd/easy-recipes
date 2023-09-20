<template>
  <VHover v-slot="hover">
    <VCard
      :width="130"
      @click="router.push({ name: 'IngredientInfo', params: { id: ingredient.id } })"
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
import type { IngredientBase } from '@/schema/ingredient';
import { stripText } from '@/utils';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps<{
  ingredient: IngredientBase;
}>();

const router = useRouter();

const ingredientName = computed(() => stripText(props.ingredient.name, 10));

const { imageSrc, onError } = useImage(props.ingredient.image_uri);
</script>

<style scoped>
.ingredient-on-hover {
  color: #40a02b;
}
</style>
