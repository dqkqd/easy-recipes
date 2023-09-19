<template>
  <DialogError
    v-model="hasError"
    title="Unable to load ingredients"
    content="Please try again later..."
    data-test="recipe-ingredients-dialog-select-error"
  />

  <VCard :width="800" :height="500">
    <VToolbar prominent>
      <VToolbarTitle
        class="mx-8 font-weight-black text-h5"
        data-test="recipe-ingredients-dialog-select-title"
        >Add more ingredients</VToolbarTitle
      >
      <VBtn
        @click="select"
        color="black"
        variant="elevated"
        class="ma-8"
        data-test="recipe-ingredients-dialog-select-add-button"
      >
        <div class="front-weight-black text-uppercase text-h6">Select</div>
      </VBtn>
    </VToolbar>
    <VCardItem>
      <div v-if="result" data-test="recipe-ingredients-dialog-select-pagination">
        <VRow class="pt-5" justify="center">
          <VCol
            v-for="ingredient in result.ingredients"
            :key="ingredient.id"
            cols="auto"
            :data-test="`recipe-ingredients-dialog-select-card-${ingredient.id}`"
          >
            <RecipeIngredientsDialogSelectCard
              :selected="selectedIngredientIds.includes(ingredient.id)"
              :ingredient-name="ingredient.name"
              :ingredient-image="ingredient.image_uri"
              @toggle-select="() => toggleSelect(ingredient.id)"
            />
          </VCol>
        </VRow>
        <VRow justify="center" class="font-weight-bold text-h3">
          <VPagination
            :length="pageLength"
            v-model="currentPage"
            data-test="recipe-ingredients-dialog-select-pagination-pagination"
          />
        </VRow>
      </div>
    </VCardItem>
  </VCard>
</template>

<script setup lang="ts">
import DialogError from '@/components/DialogError.vue';
import RecipeIngredientsDialogSelectCard from '@/components/RecipeIngredientsDialogSelectCard.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { IngredientsResponseSchema, type IngredientsResponse } from '@/schema/ingredient';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import { computed, onMounted, ref, watch } from 'vue';

const props = defineProps<{
  selectedIds: number[];
}>();

const emit = defineEmits<{
  (e: 'select', selectedIds: number[]): void;
}>();

const selectedIngredientIds = ref([...props.selectedIds]);

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
  const params = new URLSearchParams();
  params.append('per_page', `${RECIPE_INGREDIENT_PER_PAGE}`);
  if (currentPage.value !== 1) {
    params.append('page', `${currentPage.value}`);
  }

  await execute({
    method: 'get',
    url: `${apiUrl}/ingredients/`,
    params: params
  });
};

onMounted(async () => {
  getIngredientsByPages();
});

watch(currentPage, async () => {
  getIngredientsByPages();
});

function toggleSelect(id: number) {
  const index = selectedIngredientIds.value.indexOf(id);
  if (index > -1) {
    selectedIngredientIds.value.splice(index, 1);
  } else {
    selectedIngredientIds.value.push(id);
  }
}

function select() {
  emit('select', selectedIngredientIds.value);
}
</script>

<style scoped></style>
