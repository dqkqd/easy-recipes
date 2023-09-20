<template>
  <VRow justify="center">
    <VCol
      class="font-weight-black text-h5 text-center"
      cols="9"
      data-test="ingredient-recipes-title"
      >{{ titleMessage }}</VCol
    >
  </VRow>

  <div v-if="paginatedRecipes.length" data-test="ingredient-recipes-pagination">
    <VRow class="pt-5" justify="center">
      <VCol
        v-for="recipe in paginatedRecipes"
        :key="recipe.id"
        cols="auto"
        :data-test="`ingredient-recipes-pagination-${recipe.id}`"
      >
        <CardRecipe :recipe="recipe" />
      </VCol>
    </VRow>
    <VRow justify="center" class="font-weight-bold text-h3">
      <VPagination
        :length="pageLength"
        v-model="currentPage"
        data-test="ingredient-recipes-pagination-pagination"
      />
    </VRow>
  </div>
</template>

<script setup lang="ts">
import CardRecipe from '@/components/CardRecipe.vue';
import type { Ingredient } from '@/schema/ingredient';
import { INGREDIENT_RECIPE_PER_PAGE } from '@/utils';
import { computed, ref } from 'vue';

const props = defineProps<{
  ingredient: Ingredient;
}>();

const currentPage = ref(1);

const titleMessage = computed(() => {
  const totalRecipes = props.ingredient.recipes.length;
  if (totalRecipes == 0) {
    return "This ingredient hasn't been used in any recipes";
  }

  return `This ingredient is used in ${totalRecipes} ${totalRecipes === 1 ? 'recipe' : 'recipes'}`;
});

const pageLength = computed(() => {
  if (props.ingredient.recipes.length === 0) {
    return 1;
  }
  return Math.ceil(props.ingredient.recipes.length / INGREDIENT_RECIPE_PER_PAGE);
});

const paginatedRecipes = computed(() =>
  props.ingredient.recipes.slice(
    (currentPage.value - 1) * INGREDIENT_RECIPE_PER_PAGE,
    currentPage.value * INGREDIENT_RECIPE_PER_PAGE
  )
);
</script>

<style scoped></style>
