<template>
  <BaseViewBanner
    banner-image="/recipe-cover.jpg"
    banner-title="Ready to explore more recipes?"
    button-label="New Recipe"
    data-test="recipe-view-banner"
  >
    <template #button>
      <CardRecipeCreate data-test="recipe-view-banner-card-recipe-create" />
    </template>
  </BaseViewBanner>
</template>

<script setup lang="ts">
import BaseViewBanner from './BaseViewBanner.vue';
import CardRecipeCreate from './CardRecipeCreate.vue';
</script>

<style scoped></style>
