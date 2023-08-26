<template>
  <nav>
    <div>Easy Recipes</div>
  </nav>
  <RecipeView />
</template>

<script setup lang="ts">
import RecipeView from './RecipeView.vue';
</script>

<style scoped>
nav {
  font-weight: 600;
  font-size: 2rem;
  border-bottom: 2px solid #ddd;
}
</style>
