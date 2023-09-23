<template>
  <BaseViewBanner
    banner-image="/recipe-cover.jpg"
    banner-title="Ready to explore more recipes?"
    :button-label="buttonLabel"
    data-test="recipe-view-banner"
  >
    <template #button>
      <CardRecipeCreate data-test="recipe-view-banner-card-recipe-create" />
    </template>
  </BaseViewBanner>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { computed } from 'vue';
import BaseViewBanner from './BaseViewBanner.vue';
import CardRecipeCreate from './CardRecipeCreate.vue';

const user = useUserStore();
const buttonLabel = computed(() => (user.canCreateRecipe ? 'New Recipe' : undefined));
</script>

<style scoped></style>
