<template>
  <div>
    <h3>Create New Recipe</h3>
    <form @submit.prevent="submit">
      <FormInput v-model="recipe.name" label="Name" placeholder="Recipe's name" />
      <FormInput
        v-model="recipe.description"
        label="Description"
        placeholder="Recipe's description"
      />
      <FormInput v-model="recipe.image_uri" label="Image URL" placeholder="Recipe's image url" />
      <button class="submit" type="submit">Submit</button>
      <button class="close" @click="close">Close</button>
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
