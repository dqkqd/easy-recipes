<template>
  <VLayout>
    <MainAppBar />
    <VMain class="d-flex align-center justify-center">
      <VSheet :width="800" class="my-8 text-center">
        <RecipeDetails v-if="result" :recipe="result" />

        <VContainer v-else-if="isLoading">
          <VProgressCircular :size="50" indeterminate></VProgressCircular>
        </VContainer>

        <VContainer> //TODO </VContainer>
      </VSheet>
    </VMain>
  </VLayout>
</template>

<script setup lang="ts">
import MainAppBar from '@/components/navs/MainAppBar.vue';
import RecipeDetails from '@/components/recipes/RecipeDetails.vue';
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
