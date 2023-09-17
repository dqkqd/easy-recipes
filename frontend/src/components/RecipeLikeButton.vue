<template>
  <VRow align="center">
    <VBtn
      icon="mdi-heart"
      variant="tonal"
      class="mx-2"
      color="pink"
      @click="likeRecipe"
      :disabled="isLoading"
      data-test="recipe-like-button-icon"
    />
    <span class="text-body-2 font-weight-bold" data-test="recipe-like-button-text">
      {{ likedText }}
    </span>
  </VRow>
</template>

<script setup lang="ts">
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeLikedResponseSchema, type Recipe, type RecipeLikedResponse } from '@/schema/recipe';
import { computed, ref } from 'vue';

const props = defineProps<{ recipe: Recipe }>();

const { result, error, isLoading, execute } = useAxios<RecipeLikedResponse>((r) => {
  return RecipeLikedResponseSchema.parse(r.data);
});

const totalLikes = ref(props.recipe.likes);
const likedText = computed(() =>
  totalLikes.value === 0 ? 'Be the first to like this' : `${totalLikes.value} people like this`
);

async function likeRecipe() {
  await execute({
    method: 'post',
    url: `${apiUrl}/recipes/${props.recipe.id}/like`
  });

  if (!error.value && result.value) {
    totalLikes.value = result.value.total_likes;
  }
}
</script>

<style scoped></style>
