<template>
  <VDialog width="auto" v-model="hasError" data-test="recipe-details-delete-error-dialog">
    <VAlert prominent :rounded="0" justify="center" type="error" class="px-16 py-5 text-center">
      <VAlertTitle class="text-h5">Can not delete recipe</VAlertTitle>
      <div>Please try again later</div>
    </VAlert>
  </VDialog>

  <VDialog persistent width="auto" v-model="deleted" data-test="recipe-details-deleted-dialog">
    <VAlert prominent :rounded="0" justify="center" type="success" class="px-16 py-5 text-center">
      <VAlertTitle class="text-h5">Recipe deleted</VAlertTitle>
      <div>You will be redirected shortly...</div>
    </VAlert>
  </VDialog>

  <VSheet border>
    <VDialog persistent width="auto" v-model="deleting" data-test="recipe-details-deleting-dialog">
      <VProgressCircular color="red" :size="80" indeterminate />
    </VDialog>

    <VRow class="my-6 mx-3" justify="center" no-gutters>
      <VCol>
        <VImg
          :height="500"
          :max-width="500"
          :src="image_uri"
          class="align-end"
          data-test="recipe-details-image"
          cover
        >
        </VImg>
      </VCol>

      <VCol class="mx-3">
        <VSheet :height="460">
          <div
            class="font-weight-bold text-h4 text-wrap text-center"
            data-test="recipe-details-name"
          >
            {{ recipe.name }}
          </div>

          <VDivider />

          <div class="text-h6 ma-3" data-test="recipe-details-description">
            {{ recipe.description }}
          </div>
        </VSheet>

        <VRow align="center">
          <VCol cols="8" data-test="recipe-details-like">
            <VHover v-slot="{ isHovering, props }" close-delay="200">
              <VIcon
                icon="mdi-heart"
                v-bind="props"
                :color="isHovering ? 'red-darken-1' : 'red-lighten-2'"
                :size="40"
              />
              <span class="mx-2 font-weight-bold">0 people like it</span>
            </VHover>
          </VCol>

          <VCol cols="2">
            <VRow justify="center">
              <VDialog v-model="updateDialog" width="auto">
                <template v-slot:activator="{ props }">
                  <VBtn icon="mdi-pencil" v-bind="props" data-test="recipe-details-update-button" />
                </template>
                <CardRecipeUpdate :recipe="recipe" />
              </VDialog>
            </VRow>
          </VCol>

          <VCol cols="2">
            <DeleteButton
              title="Are you sure you want to delete your recipe?"
              data-test="recipe-details-delete-button"
              @accept="deleteRecipe"
            />
          </VCol>
        </VRow>
      </VCol>
    </VRow>
  </VSheet>
</template>

<script setup lang="ts">
import CardRecipeUpdate from '@/components/CardRecipeUpdate.vue';
import DeleteButton from '@/components/DeleteButton.vue';
import { useAxios } from '@/composables';
import { apiUrl, convertFileServerDev } from '@/env';
import {
  RecipeDeletedResponseSchema,
  type Recipe,
  type RecipeDeletedResponse
} from '@/schema/recipe';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps<{ recipe: Recipe }>();

const updateDialog = ref(false);
const image_uri = computed(() => {
  return convertFileServerDev(props.recipe.image_uri);
});

const router = useRouter();

const deleted = ref(false);
const hasError = ref(false);

const {
  result,
  error,
  isLoading: deleting,
  execute
} = useAxios<RecipeDeletedResponse>((r) => {
  return RecipeDeletedResponseSchema.parse(r.data);
});

async function deleteRecipe() {
  await execute({
    method: 'delete',
    url: `${apiUrl}/recipes/${props.recipe.id}`,
    headers: {
      authorization: 'bearer delete:recipe'
    }
  });

  if (!error.value && result.value) {
    deleted.value = true;
    setTimeout(() => {
      router.push({ name: 'RecipeView' });
    }, 1500);
  } else {
    hasError.value = true;
  }
}
</script>

<style scoped></style>
