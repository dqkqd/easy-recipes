<template>
  <VSheet border>
    <VRow class="my-6 mx-3" justify="center" no-gutters>
      <VCol>
        <VImg
          :height="500"
          :max-width="500"
          :src="imageSrc"
          @error="onError"
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
                <CardRecipeUpdate :recipe="recipe" @cancel="updateDialog = false" />
              </VDialog>
            </VRow>
          </VCol>

          <VCol cols="2">
            <VRow justify="center">
              <VDialog v-model="deleteDialog" width="auto">
                <template v-slot:activator="{ props }">
                  <VBtn icon="mdi-delete" v-bind="props" data-test="recipe-details-delete-button" />
                </template>
                <CardRecipeDelete :id="recipe.id" @cancel="deleteDialog = false" />
              </VDialog>
            </VRow>
          </VCol>
        </VRow>
      </VCol>
    </VRow>
  </VSheet>
</template>

<script setup lang="ts">
import CardRecipeDelete from '@/components/CardRecipeDelete.vue';
import CardRecipeUpdate from '@/components/CardRecipeUpdate.vue';
import { useImage } from '@/composables';
import { type Recipe } from '@/schema/recipe';
import { ref } from 'vue';

const props = defineProps<{ recipe: Recipe }>();

const updateDialog = ref(false);
const deleteDialog = ref(false);

const { imageSrc, onError } = useImage(props.recipe.image_uri);
</script>

<style scoped></style>
