<template>
  <VNavigationDrawer location="left" :border="false" :elevation="0" color="grey-lighten-2" />
  <VNavigationDrawer location="right" :border="false" :elevation="0" color="grey-lighten-2" />
  <VAppBar>
    <VAppBarTitle class="overflow-x-visible">
      <VBtn
        height="100vh"
        @click="router.push({ name: 'home' })"
        data-test="main-app-bar-home-button"
      >
        <a class="app-title">Easy Recipes</a>
      </VBtn>

      <VBtn
        height="100vh"
        @click="router.push({ name: 'RecipeView' })"
        text="Recipes"
        data-test="main-app-bar-recipes-button"
      />

      <VBtn
        height="100vh"
        @click="router.push({ name: 'IngredientView' })"
        text="Ingredients"
        data-test="main-app-bar-ingredients-button"
      />
    </VAppBarTitle>
    <VBtn
      v-if="auth.isLoggedIn"
      color="red-lighten-1"
      @click="logout"
      text="LOG OUT"
      class="text-h5 font-weight-black ma-2 mx-16"
      size="x-large"
      :width="200"
      data-test="base-view-banner-button"
      variant="elevated"
      density="comfortable"
    />
    <VBtn
      v-else
      color="blue-darken-1"
      @click="login"
      text="LOG IN"
      class="text-h5 font-weight-black ma-2 mx-16"
      size="x-large"
      :width="200"
      data-test="base-view-banner-button"
      variant="elevated"
      density="comfortable"
    />
  </VAppBar>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
const router = useRouter();

const auth = useAuthStore();

function login() {
  auth.login();
}

function logout() {
  auth.logout();
}
</script>

<style scoped>
.app-title {
  font-size: 30px;
  font-weight: 800;
  color: #4c4f69;
}
</style>
