<template>
  <VLayout>
    <MainAppBar />
    <VMain>
      <DialogError
        v-model="hasError"
        title="Can not load your recipe"
        content="Please try again later..."
        data-test="recipe-info-dialog-error"
      />
      <DialogLoading v-model="isLoading" data-test="recipe-info-dialog-loading" />

      <div v-if="result">
        <VRow justify="center">
          <VSheet :width="800" class="my-8 text-center">
            <RecipeDetails :recipe="result" data-test="recipe-info-recipe-details" />
          </VSheet>
        </VRow>

        <VRow justify="center">
          <VSheet :width="800" class="my-8">
            <VContainer class="align-center" data-test="recipe-info-recipe-ingredients">
              <RecipeIngredients :recipe="result" />
            </VContainer>
          </VSheet>
        </VRow>
      </div>

      <VFooter class="mt-16 pt-16" data-test="recipe-info-footer" />
    </VMain>
  </VLayout>
</template>

<script setup lang="ts">
import DialogError from '@/components/DialogError.vue';
import DialogLoading from '@/components/DialogLoading.vue';
import MainAppBar from '@/components/MainAppBar.vue';
import RecipeDetails from '@/components/RecipeDetails.vue';
import RecipeIngredients from '@/components/RecipeIngredients.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { onMounted } from 'vue';

const props = defineProps<{ id: number | string }>();

const { result, error, isLoading, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});
const { hasError } = useErrorWithTimeout(error, 2000);

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/recipes/${props.id}`
  });
});
</script>

<style scoped></style>
