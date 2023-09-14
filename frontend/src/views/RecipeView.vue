<template>
  <VApp>
    <VLayout>
      <MainAppBar />

      <VMain>
        <VContainer justify="center">
          <VRow>
            <RecipeViewBanner />
          </VRow>

          <RecipeViewPagination />
        </VContainer>

        <VFooter class="mt-16 pt-16" data-test="recipe-view-footer" />
      </VMain>
    </VLayout>
  </VApp>
</template>

<script setup lang="ts">
import MainAppBar from '@/components/MainAppBar.vue';
import RecipeViewBanner from '@/components/RecipeViewBanner.vue';
import RecipeViewPagination from '@/components/RecipeViewPagination.vue';
</script>

<style scoped></style>
