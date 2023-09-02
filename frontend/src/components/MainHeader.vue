<template>
  <VLayout class="rounded rounded-md">
    <VAppBar>
      <VAppBarTitle class="overflow-x-visible">
        <VBtn height="100vh" @click="$router.push({ name: 'home' })">
          <a class="app-title">Easy Recipes</a></VBtn
        >
        <VBtn height="100vh" @click="$router.push({ name: 'RecipeView' })" text="Recipes" />
        <VBtn height="100vh" @click="$router.push({ name: 'IngredientView' })" text="Ingredients" />
      </VAppBarTitle>
    </VAppBar>
  </VLayout>
</template>

<script setup lang="ts"></script>

<style scoped>
.app-title {
  width: 230px;
  font-size: 30px;
  font-weight: 800;
  padding: 5px;
  text-align: center;
  text-decoration: none;
  color: #4c4f69;
}
</style>
