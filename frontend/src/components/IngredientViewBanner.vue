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
import { hasPermission } from '@/auth';
import { useAuth0 } from '@auth0/auth0-vue';
import { computed, onMounted, ref, watch } from 'vue';
import BaseViewBanner from './BaseViewBanner.vue';
import CardIngredientCreate from './CardIngredientCreate.vue';

const auth = useAuth0();

const canCreateIngredient = ref(false);
const buttonLabel = computed(() => (canCreateIngredient.value ? 'New Ingredient' : undefined));

function enableCreatePermission() {
  if (auth.isAuthenticated.value) {
    auth.getAccessTokenSilently().then((token) => {
      canCreateIngredient.value = hasPermission('create:ingredient', token);
    });
  }
}

onMounted(() => {
  enableCreatePermission();
});

watch(auth.isAuthenticated, () => {
  enableCreatePermission();
});
</script>

<style scoped></style>
