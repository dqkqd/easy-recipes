<template>
  <VLayout>
    <MainAppBar />
    <VMain class="d-flex align-center justify-center">
      <VSheet :width="800" class="my-8 text-center">
        <VSheet v-if="result" border>
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
                  {{ result.name }}
                </div>

                <VDivider />

                <div class="text-h6 ma-3">
                  {{ result.description }}
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

const { result, isLoading, error, execute } = useAxios<Recipe>((r) => {
  return RecipeSchema.parse(r.data);
});

isLoading.value = true;
const image_uri = computed(() => {
  return convertFileServerDev(result.value?.image_uri);
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
