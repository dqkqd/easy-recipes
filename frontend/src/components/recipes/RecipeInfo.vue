<template>
  <VSheet border>
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
          <div class="font-weight-bold text-h4 text-wrap text-center">
            {{ recipe.name }}
          </div>

          <VDivider />

          <div class="text-h6 ma-3">
            {{ recipe.description }}
          </div>
        </VSheet>

        <VRow align="center">
          <VCol cols="8">
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
            <VBtn icon="mdi-pencil" />
          </VCol>
          <VCol cols="2">
            <VBtn icon="mdi-delete" />
          </VCol>
        </VRow>
      </VCol>
    </VRow>
  </VSheet>
</template>

<script setup lang="ts">
import { convertFileServerDev } from '@/env';
import { type Recipe } from '@/schema/recipe';
import { computed } from 'vue';

const props = defineProps<{ recipe: Recipe }>();

const image_uri = computed(() => {
  return convertFileServerDev(props.recipe.image_uri);
});
</script>

<style scoped></style>
