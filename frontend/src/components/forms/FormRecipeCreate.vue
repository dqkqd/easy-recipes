<template>
  <div>
    <h3 data-test="form-recipe-create-title">Create New Recipe</h3>
    <form @submit.prevent="submit">
      <FormInput
        v-model="recipe.name"
        label="Name"
        placeholder="Recipe's name"
        data-test="form-recipe-create-name"
      />
      <FormInput
        v-model="recipe.description"
        label="Description"
        placeholder="Recipe's description"
        data-test="form-recipe-create-description"
      />
      <FormInput
        v-model="recipe.image_uri"
        label="Image URL"
        placeholder="Recipe's image url"
        data-test="form-recipe-create-image-uri"
      />
      <button type="submit" data-test="form-recipe-create-submit">Submit</button>
      <button @click="close" data-test="form-recipe-create-close">Close</button>
    </form>
  </div>
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

<style scoped></style>
