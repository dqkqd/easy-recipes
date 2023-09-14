<template>
  <DialogError
    v-model="hasError"
    title="Unable to load ingredients"
    content="Please try again later..."
    data-test="ingredient-view-pagination-error-dialog"
  />

  <div v-if="result" data-test="ingredient-view-pagination">
    <VRow class="pt-5" justify="center">
      <VCol
        v-for="ingredient in result.ingredients"
        :key="ingredient.id"
        cols="auto"
        :data-test="`ingredient-view-pagination-${ingredient.id}`"
      >
        <CardIngredient :ingredient="ingredient" />
      </VCol>
    </VRow>
    <VRow justify="center" class="font-weight-bold text-h3">
      <VPagination
        :length="pageLength"
        v-model="currentPage"
        data-test="ingredient-view-pagination-pagination"
      />
    </VRow>
  </div>
</template>

<script setup lang="ts">
import CardIngredient from '@/components/CardIngredient.vue';
import DialogError from '@/components/DialogError.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { IngredientsResponseSchema, type IngredientsResponse } from '@/schema/ingredient';
import { computed, onMounted, ref, watch } from 'vue';

const currentPage = ref(1);

const { result, error, execute } = useAxios<IngredientsResponse>((r) => {
  return IngredientsResponseSchema.parse(r.data);
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

const getIngredientsByPages = async () => {
  await execute({
    method: 'get',
    url:
      currentPage.value === 1
        ? `${apiUrl}/ingredients/`
        : `${apiUrl}/ingredients/?page=${currentPage.value}`
  });
};

onMounted(async () => {
  getIngredientsByPages();
});

watch(currentPage, async () => {
  getIngredientsByPages();

  window.scrollTo({
    top: 0,
    left: 0,
    behavior: 'smooth'
  });
});
</script>

<style scoped></style>
