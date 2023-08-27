<template>
  <div class="container">
    <div v-if="error">Something wrong</div>
    <div v-else-if="recipesResponse">
      <span v-for="recipe in recipesResponse?.recipes" :key="recipe.id">
        <SummaryBox :recipe="recipe" />
      </span>
    </div>
    <div v-else>Loading recipes...</div>
  </div>
</template>

<script setup lang="ts">
import SummaryBox from '@/components/SummaryBox.vue';
import { getRecipes } from '@/services/recipe';
const { recipesResponse, error } = getRecipes();
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
}
span {
  display: inline-block;
}
</style>
@/services/recipe
