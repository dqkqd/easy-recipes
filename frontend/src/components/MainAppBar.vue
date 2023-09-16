<template>
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
      v-if="auth.isAuthenticated.value"
      color="black"
      @click="logout"
      text="LOG OUT"
      class="text-h5 font-weight-black ma-2 mx-16"
      size="x-large"
      data-test="base-view-banner-button"
      variant="outlined"
      density="comfortable"
    />
    <VBtn
      v-else
      color="black"
      @click="login"
      text="LOG IN"
      class="text-h5 font-weight-black ma-2 mx-16"
      size="x-large"
      data-test="base-view-banner-button"
      variant="elevated"
      density="comfortable"
    />
  </VAppBar>
</template>

<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const auth = useAuth0();

function login() {
  auth.loginWithRedirect();
}

function logout() {
  auth.logout({ logoutParams: { returnTo: window.location.origin } });
}
</script>

<style scoped>
.app-title {
  font-size: 30px;
  font-weight: 800;
  color: #4c4f69;
}
</style>
