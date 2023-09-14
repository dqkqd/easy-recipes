<template>
  <VApp>
    <VLayout>
      <MainAppBar />

      <VMain>
        <VContainer justify="center">
          <VRow>
            <IngredientViewBanner />
          </VRow>

          <IngredientViewPagination />
        </VContainer>

        <VFooter class="mt-16 pt-16" data-test="ingredient-view-footer" />
      </VMain>
    </VLayout>
  </VApp>
</template>

<script setup lang="ts">
import IngredientViewBanner from '@/components/IngredientViewBanner.vue';
import IngredientViewPagination from '@/components/IngredientViewPagination.vue';
import MainAppBar from '@/components/MainAppBar.vue';
</script>

<style scoped></style>
