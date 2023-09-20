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
import { hasPermission } from '@/auth';
import { useAuth0 } from '@auth0/auth0-vue';
import { computed, onMounted, ref, watch } from 'vue';
import BaseViewBanner from './BaseViewBanner.vue';
import CardRecipeCreate from './CardRecipeCreate.vue';

const auth = useAuth0();

const canCreateRecipe = ref(false);
const buttonLabel = computed(() => (canCreateRecipe.value ? 'New Recipe' : undefined));

function enableCreatePermission() {
  if (auth.isAuthenticated.value) {
    auth.getAccessTokenSilently().then((token) => {
      canCreateRecipe.value = hasPermission('create:recipe', token);
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
