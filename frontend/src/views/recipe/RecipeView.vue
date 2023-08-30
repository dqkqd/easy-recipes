<template>
  <div class="container">
    <div v-if="error">Something wrong</div>
    <div v-else-if="recipesResponse">
      <span v-for="recipe in recipesResponse.recipes" :key="recipe.id">
        <BoxRecipe :recipe="recipe" />
      </span>
    </div>
    <div v-else>Loading recipes...</div>
  </div>
  <button @click="showModal = !showModal">New Recipe</button>
  <Teleport to="body">
    <ModalRecipeCreate v-if="showModal" @close="showModal = false" />
  </Teleport>
</template>

<script setup lang="ts">
import BoxRecipe from '@/components/boxes/BoxRecipe.vue';
import ModalRecipeCreate from '@/components/modals/ModalRecipeCreate.vue';
import { getRecipes } from '@/services/recipe';
import { ref } from 'vue';

const { recipesResponse, error } = getRecipes();
const showModal = ref(false);
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
