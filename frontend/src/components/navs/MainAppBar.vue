<template>
  <VAppBar>
    <VAppBarTitle class="overflow-x-visible">
      <VBtn height="100vh" @click="moveToHomePage" data-test="main-app-bar-home-button">
        <a class="app-title">Easy Recipes</a></VBtn
      >

      <VBtn
        height="100vh"
        @click="moveToRecipeView"
        text="Recipes"
        data-test="main-app-bar-recipes-button"
      />

      <VBtn
        height="100vh"
        @click="moveToIngredientView"
        text="Ingredients"
        data-test="main-app-bar-ingredients-button"
      />
    </VAppBarTitle>
  </VAppBar>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function moveToHomePage() {
  router.push({ name: 'home' });
}

function moveToRecipeView() {
  router.push({ name: 'RecipeView' });
}

function moveToIngredientView() {
  router.push({ name: 'IngredientView' });
}
</script>

<style scoped>
.app-title {
  width: 230px;
  font-size: 30px;
  font-weight: 800;
  padding: 5px;
  text-align: center;
  text-decoration: none;
  color: #4c4f69;
}
</style>
