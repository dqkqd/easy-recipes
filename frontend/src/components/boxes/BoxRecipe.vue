<template>
  <VCard>
    <VCardTitle class="text-h5" data-test="box-recipe-name">{{ props.recipe.name }}</VCardTitle>
    <VAvatar :size="256" :rounded="0">
      <VImg v-if="image_uri" :src="image_uri" data-test="box-recipe-image"></VImg>
      <VImg v-else src="/no-image-icon.png" data-test="box-recipe-image"></VImg>
    </VAvatar>
    <VCardText>
      <div v-if="props.recipe.description" data-test="box-recipe-description">
        {{ props.recipe.description }}
      </div>
      <div
        v-else
        class="font-weight-light font-weight-thin font-italic"
        data-test="box-recipe-description"
      >
        No description
      </div>
    </VCardText>
    <VCardActions>
      <VBtn @click="toRecipeDetails" data-test="box-recipe-to-recipe-details-button">See more</VBtn>
    </VCardActions>
  </VCard>
</template>

<script setup lang="ts">
import { convertFileServerDev } from '@/env';
import type { Recipe } from '@/schema/recipe';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps<{
  recipe: Recipe;
}>();

const image_uri = computed(() => {
  return convertFileServerDev(props.recipe.image_uri);
});

function toRecipeDetails() {
  router.push({ name: 'RecipeDetails', params: { id: props.recipe.id } });
}
</script>

<style scoped></style>
