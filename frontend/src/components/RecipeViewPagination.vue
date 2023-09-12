<template>
  <DialogError
    v-model="hasError"
    title="Unable to load recipes"
    content="Please try again later..."
    data-test="recipe-view-pagination-error-dialog"
  />

  <div v-if="result">
    <VRow class="pt-5" justify="center">
      <VCol
        v-for="recipe in result.recipes"
        :key="recipe.id"
        cols="auto"
        :data-test="`recipe-view-pagination-${recipe.id}`"
      >
        <CardRecipe :recipe="recipe" />
      </VCol>
    </VRow>
    <VRow justify="center" class="font-weight-bold text-h3">
      <VPagination
        :length="pageLength"
        v-model="currentPage"
        data-test="recipe-view-pagination-pagination"
      />
    </VRow>
  </div>
</template>

<script setup lang="ts">
import CardRecipe from '@/components/CardRecipe.vue';
import DialogError from '@/components/DialogError.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipesResponseSchema, type RecipesResponse } from '@/schema/recipe';
import { computed, onMounted, ref, watch } from 'vue';

const currentPage = ref(1);

const { result, error, execute } = useAxios<RecipesResponse>((r) => {
  return RecipesResponseSchema.parse(r.data);
});

const hasError = ref(false);
watch(error, () => {
  if (error.value) {
    hasError.value = true;
  }
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
