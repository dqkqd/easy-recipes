<template>
  <DialogError
    v-model="hasError"
    title="Unable to load ingredients"
    content="Please try again later..."
    data-test="recipe-ingredients-pagination-error-dialog"
  />

  <DialogLoading v-model="isLoading" data-test="recipe-ingredients-loading-dialog" />

  <VRow justify="center">
    <VCol
      class="font-weight-black text-h5 text-center"
      cols="9"
      data-test="recipe-ingredients-title"
      >{{ titleMessage }}</VCol
    >

    <VCol cols="3" align="center">
      <VBtn
        class="text-body-2"
        color="black"
        text="Add more ingredients"
        data-test="recipe-ingredients-add-ingredients-button"
      />
    </VCol>
  </VRow>

  <div v-if="result && result.total" data-test="recipe-ingredients-pagination">
    <VRow class="pt-5" justify="center">
      <VCol
        v-for="ingredient in result.ingredients"
        :key="ingredient.id"
        cols="auto"
        :data-test="`recipe-ingredients-pagination-${ingredient.id}`"
      >
        <CardIngredient :ingredient="ingredient" />
      </VCol>
    </VRow>
    <VRow justify="center" class="font-weight-bold text-h3">
      <VPagination
        :length="pageLength"
        v-model="currentPage"
        data-test="recipe-ingredients-pagination-pagination"
      />
    </VRow>
  </div>
</template>

<script setup lang="ts">
import CardIngredient from '@/components/CardIngredient.vue';
import DialogError from '@/components/DialogError.vue';
import DialogLoading from '@/components/DialogLoading.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { IngredientsResponseSchema, type IngredientsResponse } from '@/schema/ingredient';
import { computed, onMounted, ref, watch } from 'vue';

const props = defineProps<{
  id: number;
}>();

const currentPage = ref(1);

const { result, error, isLoading, execute } = useAxios<IngredientsResponse>((r) => {
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
        ? `${apiUrl}/recipes/${props.id}/ingredients/`
        : `${apiUrl}/recipes/${props.id}/ingredients/?page=${currentPage.value}`
  });
};

const titleMessage = computed(() => {
  if (result.value?.total === 0) {
    return 'This recipe is made without any ingredients';
  }
  return 'This recipe is made using these ingredients';
});

onMounted(async () => {
  getIngredientsByPages();
});

watch(currentPage, async () => {
  getIngredientsByPages();
});
</script>

<style scoped></style>
