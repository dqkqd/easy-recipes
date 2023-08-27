<template>
  <div class="modal-mask">
    <div class="modal-container">
      <h3>Create New Recipe</h3>
      <form>
        <FormInput v-model="recipeCreate.name" label="Name" value="" />
        <FormInput v-model="recipeCreate.description" label="Description" value="" />
        <FormInput v-model="recipeCreate.image_uri" label="Image URL" value="" />
      </form>
      <button @click="onSubmit">Submit</button>
      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import FormInput from '@/components/forms/FormInput.vue';
import { createRecipe } from '@/services/recipe';
const emit = defineEmits<{
  (e: 'close'): void;
}>();

const { recipeCreate, create } = createRecipe();

function onSubmit() {
  create();
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
