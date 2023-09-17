<template>
  <VLayout>
    <MainAppBar />
    <VMain>
      <VRow justify="center">
        <VSheet :width="800" class="my-8 text-center">
          <RecipeDetails v-if="result" :recipe="result" />

          <VContainer v-else-if="isLoading">
            <VProgressCircular :size="50" indeterminate />
          </VContainer>
        </VSheet>
      </VRow>

      <VRow justify="center">
        <VSheet :width="800" class="my-8">
          <VContainer class="align-center">
            <RecipeIngredients v-if="result" :id="result.id" />
          </VContainer>
        </VSheet>
      </VRow>
    </VMain>
  </VLayout>
</template>

<script setup lang="ts">
import MainAppBar from '@/components/MainAppBar.vue';
import RecipeDetails from '@/components/RecipeDetails.vue';
import RecipeIngredients from '@/components/RecipeIngredients.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { onMounted } from 'vue';

const props = defineProps<{ id: number | string }>();

const { result, isLoading, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/${props.id}`
  });
});
</script>

<style scoped></style>
