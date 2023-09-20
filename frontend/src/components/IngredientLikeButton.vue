<template>
  <VRow align="center">
    <VBtn
      icon="mdi-heart"
      variant="tonal"
      class="mx-2"
      color="pink"
      @click="likeIngredient"
      :disabled="isLoading"
      data-test="ingredient-like-button-icon"
    />
    <span class="text-body-2 font-weight-bold" data-test="ingredient-like-button-text">
      {{ likedText }}
    </span>
  </VRow>
</template>

<script setup lang="ts">
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import {
  IngredientLikedResponseSchema,
  type IngredientBase,
  type IngredientLikedResponse
} from '@/schema/ingredient';
import { computed, ref } from 'vue';

const props = defineProps<{ ingredient: IngredientBase }>();

const { result, error, isLoading, execute } = useAxios<IngredientLikedResponse>((r) => {
  return IngredientLikedResponseSchema.parse(r.data);
});

const totalLikes = ref(props.ingredient.likes);
const likedText = computed(() =>
  totalLikes.value === 0 ? 'Be the first to like this' : `${totalLikes.value} people like this`
);

async function likeIngredient() {
  await execute({
    method: 'post',
    url: `${apiUrl}/ingredients/${props.ingredient.id}/like`
  });

  if (!error.value && result.value) {
    totalLikes.value = result.value.total_likes;
  }
}
</script>

<style scoped></style>
