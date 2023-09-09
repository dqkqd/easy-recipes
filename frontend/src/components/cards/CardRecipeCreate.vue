<template>
  <VSheet :width="800">
    <VCard class="px-5 pb-8">
      <VCardTitle
        class="text-center my-8 py-1 font-weight-black text-h4"
        data-test="card-recipe-create-title"
        >Add new recipe</VCardTitle
      >

      <FormRecipeCreate data-test="card-recipe-create-form-recipe" />
    </VCard>
  </VSheet>
</template>

<script setup lang="ts">
import FormRecipeCreate from '../forms/FormRecipeCreate.vue';
</script>

<style scoped></style>
