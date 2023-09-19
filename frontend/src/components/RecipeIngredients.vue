<template>
  <VRow justify="center">
    <VCol
      class="font-weight-black text-h5 text-center"
      cols="9"
      data-test="recipe-ingredients-title"
      >{{ titleMessage }}</VCol
    >

    <VCol v-if="canUpdateRecipe" cols="3" align="center">
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
import { hasPermission } from '@/auth';
import CardIngredient from '@/components/CardIngredient.vue';
import RecipeIngredientsDialog from '@/components/RecipeIngredientsDialog.vue';
import type { IngredientBase } from '@/schema/ingredient';
import type { Recipe } from '@/schema/recipe';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import { useAuth0 } from '@auth0/auth0-vue';
import { computed, onMounted, ref, watch } from 'vue';

const props = defineProps<{
  recipe: Recipe;
}>();

const auth = useAuth0();
const canUpdateRecipe = ref(false);
function enableUpdatePermission() {
  if (auth.isAuthenticated.value) {
    auth.getAccessTokenSilently().then((token) => {
      canUpdateRecipe.value = hasPermission('update:recipe', token);
    });
  }
}

onMounted(async () => {
  enableUpdatePermission();
});

watch(auth.isAuthenticated, () => {
  enableUpdatePermission();
});

const currentPage = ref(1);

const selectedIngredients = ref(props.recipe.ingredients);
const selectedIngredientIds = computed(() =>
  selectedIngredients.value.map((ingredient) => ingredient.id)
);

function updatedIngredients(ingredients: IngredientBase[]) {
  selectedIngredients.value = ingredients;
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