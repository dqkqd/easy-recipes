<template>
  <VAppBar>
    <VAppBarTitle class="overflow-x-visible">
      <VBtn
        height="100vh"
        @click="router.push({ name: 'home' })"
        data-test="main-app-bar-home-button"
      >
        <a class="app-title">Easy Recipes</a>
      </VBtn>

      <VBtn
        height="100vh"
        @click="router.push({ name: 'RecipeView' })"
        text="Recipes"
        data-test="main-app-bar-recipes-button"
      />

      <VBtn
        height="100vh"
        @click="router.push({ name: 'IngredientView' })"
        text="Ingredients"
        data-test="main-app-bar-ingredients-button"
      />
    </VAppBarTitle>
  </VAppBar>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();
</script>

<style scoped>
.app-title {
  font-size: 30px;
  font-weight: 800;
  color: #4c4f69;
}
</style>
