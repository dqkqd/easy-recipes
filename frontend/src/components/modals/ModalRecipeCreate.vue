<template>
  <div class="modal-mask">
    <div class="modal-container">
      <FormRecipeCreate @submit="createNewRecipe" @close="$emit('close')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { RecipeCreate } from '@/interfaces/recipe';
import { useRouter } from 'vue-router';
import FormRecipeCreate from '../forms/FormRecipeCreate.vue';

const router = useRouter();
async function createNewRecipe(recipeCreate: RecipeCreate) {
  const { id, error } = await recipeCreate.insert();
  if (!error.value) {
    router.push(`/recipes/${id.value}`);
  }
}
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 300px;
  margin: auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}
</style>
