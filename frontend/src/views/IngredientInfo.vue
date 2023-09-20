<template>
  <VLayout>
    <MainAppBar />
    <VMain>
      <DialogError
        v-model="hasError"
        title="Can not load your ingredient"
        content="Please try again later..."
        data-test="ingredient-info-dialog-error"
      />
      <DialogLoading v-model="isLoading" data-test="ingredient-info-dialog-loading" />

      <div v-if="result">
        <VRow justify="center" class="my-16">
          <IngredientDetails :ingredient="result" />
        </VRow>

        <VRow justify="center">
          <VSheet :width="800" class="my-8">
            <VContainer class="align-center" data-test="recipe-info-recipe-ingredients">
              <IngredientRecipes :ingredient="result" />
            </VContainer>
          </VSheet>
        </VRow>
      </div>
    </VMain>
  </VLayout>
</template>

<script setup lang="ts">
import IngredientDetails from '@/components/IngredientDetails.vue';
import IngredientRecipes from '@/components/IngredientRecipes.vue';
import MainAppBar from '@/components/MainAppBar.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import { IngredientSchema, type Ingredient } from '@/schema/ingredient';
import { onMounted } from 'vue';

const props = defineProps<{ id: number | string }>();

const { result, error, isLoading, execute } = useAxios<Ingredient>((r) => {
  return IngredientSchema.parse(r.data);
});

const { hasError } = useErrorWithTimeout(error, 2000);

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/ingredients/${props.id}`
  });
});
</script>

<style scoped></style>
