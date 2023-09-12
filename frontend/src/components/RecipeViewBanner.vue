<template>
  <VImg
    src="/recipe-cover.jpg"
    :max-height="220"
    gradient="to left, rgba(0,0,0,.1), rgba(0,0,0,.7)"
    cover
    data-test="recipe-view-banner-cover-image"
  >
    <VRow no-gutters class="py-10" justify="center" align-content="center" align="center">
      <VCol cols="9" align-self="center">
        <div
          class="text-h2 mx-16 font-weight-black text-white me-auto"
          data-test="recipe-view-banner-title"
        >
          Ready to explore more recipes?
        </div>
      </VCol>
      <VCol cols="3" align-self="center">
        <VDialog v-model="dialog" scrollable width="auto">
          <template v-slot:activator="{ props }">
            <VBtn
              color="black"
              v-bind="props"
              text="New Recipe"
              class="text-h5 font-weight-black"
              size="x-large"
              data-test="recipe-view-banner-new-recipe-button"
            />
          </template>
          <CardRecipeCreate
            data-test="recipe-view-banner-card-recipe-create"
            @cancel="dialog = false"
          />
        </VDialog>
      </VCol>
    </VRow>
  </VImg>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import CardRecipeCreate from './CardRecipeCreate.vue';
const dialog = ref(false);
</script>

<style scoped></style>
