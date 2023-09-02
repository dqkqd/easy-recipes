<template>
  <VApp>
    <MainAppBar />
    <VMain>
      <div class="content-body">
        <div v-if="error" data-test="recipe-view-error">Something wrong ...</div>
        <div v-else-if="result" data-test="recipe-view-result">
          <span v-for="recipe in result.recipes" :key="recipe.id">
            <CardRecipe :recipe="recipe" />
          </span>
        </div>
        <div v-else data-test="recipe-view-loading">Loading ...</div>
      </div>

      <VBtn @click="showModal = true" data-test="recipe-view-new-button" text="New Recipe"></VBtn>

      <Teleport to="body">
        <ModalRecipeCreate v-if="showModal" @close="showModal = false" />
      </Teleport>
    </VMain>
  </VApp>
</template>

<script setup lang="ts">
import MainAppBar from '@/components/MainAppBar.vue';
import CardRecipe from '@/components/cards/CardRecipe.vue';
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
