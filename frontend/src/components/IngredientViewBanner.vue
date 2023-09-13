<template>
  <BaseViewBanner
    banner-image="/ingredient-cover.jpg"
    banner-title="Ready to explore more ingredients?"
    button-label="New Ingredient"
    data-test="ingredient-view-banner"
  >
    <template #button>
      <CardIngredientCreate data-test="ingredient-view-banner-card-ingredient-create" />
    </template>
  </BaseViewBanner>
</template>

<script setup lang="ts">
import BaseViewBanner from './BaseViewBanner.vue';
import CardIngredientCreate from './CardIngredientCreate.vue';
</script>

<style scoped></style>
