<template>
  <HomeTitle />
  <div class="content-body">
    <div v-if="error" data-test="recipe-view-error">Something wrong ...</div>
    <div v-else-if="result" data-test="recipe-view-result">
      <span v-for="recipe in result.recipes" :key="recipe.id">
        <BoxRecipe :recipe="recipe" />
      </span>
    </div>
    <div v-else data-test="recipe-view-loading">Loading ...</div>
  </div>
  <button @click="showModal = true" data-test="recipe-view-new-button">New Recipe</button>
  <Teleport to="body">
    <ModalRecipeCreate v-if="showModal" @close="showModal = false" />
  </Teleport>
</template>

<script setup lang="ts">
import HomeTitle from '@/components/HomeTitle.vue';
import BoxRecipe from '@/components/boxes/BoxRecipe.vue';
import ModalRecipeCreate from '@/components/modals/ModalRecipeCreate.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipesResponseSchema, type RecipesResponse } from '@/schema/recipe';
import { onMounted, ref } from 'vue';

const showModal = ref(false);

const { result, error, execute } = useAxios<RecipesResponse>((r) => {
  return RecipesResponseSchema.parse(r.data);
});

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/`
  });
});
</script>

<style scoped>
.content-body {
  display: flex;
  flex-wrap: wrap;
}
span {
  display: inline-block;
}
</style>
