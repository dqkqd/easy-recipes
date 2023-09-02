<template>
  <VApp>
    <MainAppBar />
    <VMain>
      <div v-if="error" data-test="recipe-view-error">Something wrong ...</div>

      <div v-else-if="result" data-test="recipe-view-result">
        <div class="d-flex flex-wrap">
          <VSheet rounded v-for="recipe in result.recipes" :key="recipe.id" class="pa-2 ma-2">
            <CardRecipe :recipe="recipe" />
          </VSheet>
        </div>

        <VBtn @click="showModal = true" data-test="recipe-view-new-button" text="New Recipe"></VBtn>

        <Teleport to="body">
          <ModalRecipeCreate v-if="showModal" @close="showModal = false" />
        </Teleport>
      </div>

      <div v-else data-test="recipe-view-loading">
        <VProgressLinear indeterminate color="blue"></VProgressLinear>
      </div>
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

<style scoped></style>
