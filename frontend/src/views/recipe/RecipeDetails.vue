<template>
  <VLayout>
    <MainAppBar />
    <VMain class="d-flex align-center justify-center">
      <VSheet :width="800" class="my-8 text-center">
        <RecipeInfo v-if="result" :recipe="result" />

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
import RecipeInfo from '@/components/recipes/RecipeInfo.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import {
  RecipeDeletedResponseSchema,
  RecipeSchema,
  type Recipe,
  type RecipeDeletedResponse
} from '@/schema/recipe';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{ id: number | string }>();

const { result, isLoading, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});

const {
  result: deletedResult,
  error: deletedError,
  isLoading: isDeleteing,
  execute: deleteExec
} = useAxios<RecipeDeletedResponse>((r) => {
  return RecipeDeletedResponseSchema.parse(r.data);
});

async function deleteRecipe() {
  await deleteExec({
    method: 'delete',
    url: `${apiUrl}/recipes/${props.id}`,
    headers: {
      authorization: 'bearer delete:recipe'
    }
  });

  if (!deletedError.value && deletedResult.value) {
    router.push({ name: 'home' });
  }
}

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/${props.id}`
  });
});
</script>

<style scoped>
.v-icon {
  transition: opacity 0.4s ease-in-out;
}
.v-icon:not(.on-hover) {
  opacity: 0.8;
}
</style>
