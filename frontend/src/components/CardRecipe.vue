<template>
  <VHover v-slot="hover">
    <VCard
      :width="200"
      @click="router.push({ name: 'RecipeInfo', params: { id: recipe.id } })"
      :elevation="hover && hover.isHovering ? 12 : 2"
      data-test="card-to-recipe-details"
      v-bind="hover && hover.props"
      :class="{ 'recipe-on-hover': hover && hover.isHovering }"
    >
      <VImg
        :src="imageSrc"
        @error="onError"
        :height="180"
        :width="200"
        lazy-src="/recipe-cover.jpg"
        cover
        data-test="card-recipe-image"
      />

      <VCardTitle class="text-center font-weight-bold" data-test="card-recipe-name">
        {{ recipeName }}
      </VCardTitle>
    </VCard>
  </VHover>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import type { RecipeBase } from '@/schema/recipe';
import { stripText } from '@/utils';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{
  recipe: RecipeBase;
}>();

const recipeName = computed(() => stripText(props.recipe.name, 20));

const { imageSrc, onError } = useImage(props.recipe.image_uri);
</script>

<style scoped>
.recipe-on-hover {
  color: #40a02b;
}
</style>
