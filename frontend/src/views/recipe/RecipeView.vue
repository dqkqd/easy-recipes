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

        <VRow justify="center">
          <VDialog v-model="dialog" scrollable width="auto">
            <template v-slot:activator="{ props }">
              <VBtn v-bind="props">New Recipe</VBtn></template
            >
            <CardRecipeCreate />
          </VDialog>
        </VRow>

        <VPagination
          :length="pageLength"
          v-model="currentPage"
          data-test="recipe-view-pagination"
        ></VPagination>
      </div>

      <div v-else data-test="recipe-view-loading">
        <VProgressLinear indeterminate color="blue"></VProgressLinear>
      </div>
    </VMain>
  </VApp>
</template>

<script setup lang="ts">
import CardRecipe from '@/components/cards/CardRecipe.vue';
import CardRecipeCreate from '@/components/cards/CardRecipeCreate.vue';
import MainAppBar from '@/components/navs/MainAppBar.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipesResponseSchema, type RecipesResponse } from '@/schema/recipe';
import { computed, onMounted, ref, watch } from 'vue';

const currentPage = ref(1);

const dialog = ref(false);

const { result, error, execute } = useAxios<RecipesResponse>((r) => {
  return RecipesResponseSchema.parse(r.data);
});

const pageLength = computed(() => {
  if (!result.value || result.value.per_page === 0) {
    return 1;
  }
  return Math.ceil(result.value.total / result.value.per_page);
});

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/`
  });
});

watch(currentPage, async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/?page=${currentPage.value}`
  });
  window.scrollTo({
    top: 0,
    left: 0,
    behavior: 'smooth'
  });
});
</script>

<style scoped></style>
