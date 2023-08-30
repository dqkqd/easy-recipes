<template>
  <div class="modal-mask">
    <div class="modal-container">
      <div v-if="error" data-test="modal-recipe-create-error">Something wrong ...</div>
      <div v-else-if="isLoading" data-test="modal-recipe-create-loading">Loading ...</div>
      <FormRecipeCreate
        v-else
        @submit="submit"
        @close="$emit('close')"
        data-test="modal-recipe-create-form"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAxios } from '@/composables/fetch';
import { apiUrl } from '@/env';
import { type RecipeCreate } from '@/interfaces/recipe';
import { RecipeCreatedResponseSchema } from '@/validator/recipe';
import { useRouter } from 'vue-router';
import FormRecipeCreate from '../forms/FormRecipeCreate.vue';

const router = useRouter();
const { result, error, isLoading, execute } = useAxios<number>((r) => {
  const { id } = RecipeCreatedResponseSchema.parse(r.data);
  return id;
});

async function submit(recipeCreate: RecipeCreate) {
  await execute({
    method: 'post',
    url: `${apiUrl}/recipes/`,
    data: recipeCreate,
    headers: {
      authorization: 'bearer create:recipe'
    }
  });

  if (!error.value && result.value) {
    router.push({ name: 'RecipeDetails', params: { id: result.value } });
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
