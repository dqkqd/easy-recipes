<template>
  <div class="container">
    <div v-if="hasResponse">
      <span v-for="recipe in recipesResponse?.recipes" :key="recipe.id">
        <SummaryBox :recipe="recipe" />
      </span>
    </div>
    <div v-else>Loading recipes...</div>
  </div>
</template>

<script setup lang="ts">
import SummaryBox from '@/components/SummaryBox.vue';
import { apiUrl } from '@/env';
import { RecipesResponseSchema } from '@/validator/recipe';
import { computed, onMounted, ref } from 'vue';

const recipesResponse = ref();
const hasResponse = computed(() => recipesResponse.value && recipesResponse.value.recipes.length);
onMounted(() => {
  fetch(`${apiUrl}/recipes`)
    .then((res) => res.json())
    .then((res) => {
      recipesResponse.value = RecipesResponseSchema.parse(res);
    })
    .catch((err) => console.log(err));
});
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
}
span {
  display: inline-block;
}
</style>
