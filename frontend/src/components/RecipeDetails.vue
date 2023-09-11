<template>
  <VSheet border>
    <VRow class="my-6 mx-3" no-gutters>
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
        <VSheet :height="460" :max-width="400">
          <VCard :elevation="0">
            <VCardTitle class="text-h4 font-weight-black">
              {{ recipeDetails.name }}
            </VCardTitle>
            <VDivider />
            <VCardText class="text-left text-body-1">
              {{ recipeDetails.description }}
            </VCardText>
          </VCard>
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
              <VDialog v-model="updateDialog" width="auto" data-test="recipe-details-update-dialog">
                <template v-slot:activator="{ props }">
                  <VBtn icon="mdi-pencil" v-bind="props" data-test="recipe-details-update-button" />
                </template>
                <CardRecipeUpdate
                  @updated="updated"
                  :recipe="recipeDetails"
                  @cancel="closeUpdateDialog"
                />
              </VDialog>

              <DialogSuccess
                v-model="recipeUpdated"
                title="Recipe updated"
                data-test="card-recipe-update-updated-dialog"
              />
            </VRow>
          </VCol>

          <VCol cols="2">
            <VRow justify="center">
              <VDialog v-model="deleteDialog" width="auto" data-test="recipe-details-delete-dialog">
                <template v-slot:activator="{ props }">
                  <VBtn icon="mdi-delete" v-bind="props" data-test="recipe-details-delete-button" />
                </template>
                <CardRecipeDelete :id="recipe.id" @cancel="closeDeleteDialog" />
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
import DialogSuccess from '@/components/DialogSuccess.vue';
import { useImage } from '@/composables';
import { type Recipe } from '@/schema/recipe';
import { ref } from 'vue';

const props = defineProps<{ recipe: Recipe }>();

const recipeUpdated = ref(false);

const recipeDetails = ref({ ...props.recipe });
const recipeImage = ref(recipeDetails.value.image_uri);

const { imageSrc, onError } = useImage(recipeDetails.value.image_uri, recipeImage);

const updateDialog = ref(false);
function closeUpdateDialog() {
  updateDialog.value = false;
}

const deleteDialog = ref(false);
function closeDeleteDialog() {
  deleteDialog.value = false;
}

async function updated(name: string, image: string | null, description: string) {
  recipeDetails.value.name = name;
  recipeDetails.value.description = description;
  recipeDetails.value.image_uri = image;
  recipeImage.value = image;
  closeUpdateDialog();

  setTimeout(() => {
    recipeUpdated.value = true;
    setTimeout(() => {
      recipeUpdated.value = false;
    }, 500);
  }, 50);
}
</script>

<style scoped></style>
