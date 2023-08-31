<template>
  <div>
    <h3 data-test="form-recipe-create-title">Create New Recipe</h3>
    <form @submit.prevent="submit">
      <FormInput
        v-model="name"
        label="Name"
        placeholder="Recipe's name"
        data-test="form-recipe-create-name"
      />
      <FormInput
        v-model="description"
        label="Description"
        placeholder="Recipe's description"
        data-test="form-recipe-create-description"
      />
      <FormInput
        v-model="image_uri"
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
import { RecipeCreateSchema, type RecipeCreate } from '@/schema/recipe';
import { ref } from 'vue';

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', recipe: RecipeCreate): void;
}>();

const name = ref('');
const description = ref(null);
const image_uri = ref(null);

function submit() {
  emit(
    'submit',
    RecipeCreateSchema.parse({
      name: name.value,
      description: description.value,
      image_uri: image_uri.value
    })
  );
}

function close() {
  emit('close');
}
</script>

<style scoped></style>
@/schema/recipe
