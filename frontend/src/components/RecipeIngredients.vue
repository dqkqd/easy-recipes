<template>
  <VRow justify="center">
    <VCol
      class="font-weight-black text-h5 text-center"
      cols="9"
      data-test="recipe-ingredients-title"
      >{{ titleMessage }}</VCol
    >

    <VCol v-if="user.canUpdateRecipe" cols="3" align="center">
      <RecipeIngredientsDialog
        :recipeId="recipe.id"
        :selectedIngredientIds="selectedIngredientIds"
        @updated="updatedIngredients"
      />
    </VCol>
  </VRow>

  <div v-if="paginatedIngredients.length" data-test="recipe-ingredients-pagination">
    <VRow class="pt-5" justify="center">
      <VCol
        v-for="ingredient in paginatedIngredients"
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
import RecipeIngredientsDialog from '@/components/RecipeIngredientsDialog.vue';
import type { IngredientBase } from '@/schema/ingredient';
import type { Recipe } from '@/schema/recipe';
import { useUserStore } from '@/stores/user';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import { computed, ref } from 'vue';

const props = defineProps<{
  recipe: Recipe;
}>();

const user = useUserStore();

const currentPage = ref(1);

const selectedIngredients = ref(props.recipe.ingredients);
const selectedIngredientIds = computed(() =>
  selectedIngredients.value.map((ingredient) => ingredient.id)
);

function updatedIngredients(ingredients: IngredientBase[]) {
  selectedIngredients.value = [...ingredients].sort((a, b) => a.id - b.id);
  currentPage.value = 1;
}

const titleMessage = computed(() => {
  if (selectedIngredients.value.length === 0) {
    return 'This recipe is made without any ingredients';
  }
  return 'This recipe is made using these ingredients';
});

const pageLength = computed(() => {
  if (selectedIngredients.value.length === 0) {
    return 1;
  }
  return Math.ceil(selectedIngredients.value.length / RECIPE_INGREDIENT_PER_PAGE);
});

const paginatedIngredients = computed(() =>
  selectedIngredients.value.slice(
    (currentPage.value - 1) * RECIPE_INGREDIENT_PER_PAGE,
    currentPage.value * RECIPE_INGREDIENT_PER_PAGE
  )
);
</script>

<style scoped></style>
