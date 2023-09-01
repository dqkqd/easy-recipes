<template>
  <MainHeader />
  <div v-if="error" data-test="recipe-details-error">Something wrong ...</div>
  <div v-else-if="result">
    <h1 data-test="recipe-details-name">{{ result.name }}</h1>
    <p data-test="recipe-details-description">{{ result.description }}</p>
    <img v-if="image_uri" :src="image_uri" data-test="recipe-details-valid-image" />
    <img v-else src="/no-image-icon.png" data-test="recipe-details-default-image" />
    <div>
      <DeleteButton label="Delete recipe" @close="deleteRecipe" />
      <div v-if="deletedError" data-test="recipe-details-delete-error">
        Error while deleting ...
      </div>
      <div v-else-if="isDeleteing" data-test="recipe-details-delete-loading">Deleting ...</div>
    </div>
  </div>
  <div v-else data-test="recipe-details-loading">Loading ...</div>
</template>

<script setup lang="ts">
import MainHeader from '@/components/MainHeader.vue';
import DeleteButton from '@/components/buttons/DeleteButton.vue';
import { useAxios } from '@/composables';
import { apiUrl, convertFileServerDev } from '@/env';
import {
  RecipeDeletedResponseSchema,
  RecipeSchema,
  type Recipe,
  type RecipeDeletedResponse
} from '@/schema/recipe';
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{ id: number | string }>();

const { result, error, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});

const image_uri = computed(() => {
  if (result.value) {
    return convertFileServerDev(result.value?.image_uri);
  }
  return null;
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

<style scoped></style>
@/schema/recipe
