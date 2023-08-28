<template>
  <h3>Create New Recipe</h3>
  <form @submit.prevent="submit">
    <FormInput v-model="recipe.name" label="Name" value="" />
    <FormInput v-model="recipe.description" label="Description" value="" />
    <FormInput v-model="recipe.image_uri" label="Image URL" value="" />
    <button @click="submit">Submit</button>
    <button @click="close">Close</button>
  </form>
</template>

<script setup lang="ts">
import FormInput from '@/components/forms/FormInput.vue';
import { RecipeCreate } from '@/interfaces/recipe';
import { ref } from 'vue';

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', recipe: RecipeCreate): void;
}>();

const recipe = ref<RecipeCreate>(new RecipeCreate('', null, null));

async function submit() {
  emit('submit', recipe.value);
}

async function close() {
  emit('close');
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
