<template>
  <BaseViewBanner
    banner-image="/ingredient-cover.jpg"
    banner-title="Ready to explore more ingredients?"
    :button-label="buttonLabel"
    data-test="ingredient-view-banner"
  >
    <template #button>
      <CardIngredientCreate data-test="ingredient-view-banner-card-ingredient-create" />
    </template>
  </BaseViewBanner>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { computed } from 'vue';
import BaseViewBanner from './BaseViewBanner.vue';
import CardIngredientCreate from './CardIngredientCreate.vue';

const user = useUserStore();
const buttonLabel = computed(() => (user.canCreateIngredient ? 'New Ingredient' : undefined));
</script>

<style scoped></style>
