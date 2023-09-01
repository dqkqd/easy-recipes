<template>
  <div class="main-header">
    <router-link :to="{ name: 'home' }" class="app-title text-scale-on-hover"
      >Easy Recipes</router-link
    >
    <nav class="app-content">
      <router-link :to="{ name: 'RecipeView' }" class="app-content-link text-scale-on-hover"
        >Recipes</router-link
      >
      <router-link :to="{ name: 'IngredientView' }" class="app-content-link text-scale-on-hover"
        >Ingredients</router-link
      >
    </nav>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.main-header {
  display: flex;
  align-items: center;
  padding-bottom: 10px;
  background-color: #dce0e8;
}

.app-title {
  width: 230px;
  font-size: 30px;
  font-weight: 800;
  padding: 5px;
  text-align: center;
  text-decoration: none;
  color: #4c4f69;
}

.app-content {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.app-content-link {
  padding-left: 30px;
  height: 100%;
  font-size: 20px;
  text-decoration: none;
  padding: 0 10px;
  color: #4c4f69;
}

.text-scale-on-hover:hover {
  transform: scale(1.05);
}
</style>
