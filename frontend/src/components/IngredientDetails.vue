<template>
  <VSheet border data-test="ingredient-details">
    <VRow class="my-6 mx-3" no-gutters>
      <VCol>
        <VImg
          :height="230"
          :max-width="200"
          :src="imageSrc"
          @error="onError"
          class="align-end"
          data-test="ingredient-details-image"
          cover
        >
        </VImg>
      </VCol>

      <VCol class="mx-3">
        <VSheet :height="200" :max-width="300">
          <VCard :elevation="0">
            <VCardTitle class="text-h6 font-weight-black" data-test="ingredient-details-name">
              {{ ingredient.name }}
            </VCardTitle>
            <VDivider />
            <VCardText class="text-left text-body-2" data-test="ingredient-details-description">
              {{ ingredient.description }}
            </VCardText>
          </VCard>
        </VSheet>
        <IngredientLikeButton :ingredient="ingredient" data-test="ingredient-details-like-button" />
      </VCol>
    </VRow>
  </VSheet>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import { type IngredientBase } from '@/schema/ingredient';
import IngredientLikeButton from './IngredientLikeButton.vue';

const props = defineProps<{ ingredient: IngredientBase }>();
const { imageSrc, onError } = useImage(props.ingredient.image_uri);
</script>

<style scoped></style>
