<template>
  <VSheet border data-test="ingredient-details">
    <VRow class="my-6 mx-3" no-gutters>
      <VCol>
        <VImg
          :height="200"
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

        <VRow align="center" justify="end" data-test="ingredient-details-like">
          <VHover v-slot="{ isHovering, props }" close-delay="200">
            <VIcon
              icon="mdi-heart"
              v-bind="props"
              :color="isHovering ? 'red-darken-1' : 'red-lighten-2'"
              :size="40"
            />
            <span class="mx-2 font-weight-bold">0 people like this</span>
          </VHover>
        </VRow>
      </VCol>
    </VRow>
  </VSheet>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import { type Ingredient } from '@/schema/ingredient';

const props = defineProps<{ ingredient: Ingredient }>();
const { imageSrc, onError } = useImage(props.ingredient.image_uri);
</script>

<style scoped></style>
