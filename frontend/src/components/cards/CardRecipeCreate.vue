<template>
  <VSheet :width="800">
    <VCard class="px-5 pb-8">
      <VCardTitle
        class="text-center my-8 py-1 font-weight-black text-h4"
        data-test="card-recipe-create-title"
        >Add new recipe</VCardTitle
      >

      <VForm :disabled="isLoading" fast-fail @submit.prevent="createRecipe">
        <VTextField
          variant="solo-filled"
          v-model="recipe.name"
          clearable
          label="Name *"
          required
          :rules="[required('Name')]"
          class="pb-4"
          data-test="card-form-recipe-create-name"
        />

        <VTextField
          variant="solo-filled"
          v-model="recipe.image_uri"
          clearable
          label="Image URL *"
          hint="Please provide the best image to describe your recipe"
          :rules="[validateURL]"
          class="pb-4"
          data-test="card-form-recipe-create-image-uri"
        />

        <VTextarea
          variant="underlined"
          v-model="recipe.description"
          clearable
          label="Description"
          hint="Please provide the best description to describe your recipe"
          density="compact"
          class="pb-4"
          data-test="card-form-recipe-create-description"
        />

        <VBtn
          type="submit"
          :loading="isLoading"
          block
          color="#4f545c"
          elevation="5"
          class="text-h5 text-center"
          size="x-large"
          prepend-icon="mdi-plus"
          data-test="card-form-recipe-create-submit-button"
          text="ADD"
        />

        <VDialog v-model="hasError" :width="500" transition="fade-transition">
          <CardError data-test="card-form-recipe-create-error">
            <template v-slot:error-message>Can't add new recipe. Please try again.</template>
          </CardError>
        </VDialog>
      </VForm>
    </VCard>
  </VSheet>
</template>

<script setup lang="ts">
import CardError from '@/components/cards/CardError.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import {
  RecipeCreatedResponseSchema,
  type RecipeCreate,
  type RecipeCreatedResponse
} from '@/schema/recipe';
import { required, validateURL } from '@/validators';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import type { SubmitEventPromise } from 'vuetify';

const recipe = ref<RecipeCreate>({ name: '', description: null, image_uri: null });

const router = useRouter();
const { result, isLoading, error, execute } = useAxios<RecipeCreatedResponse>((r) => {
  return RecipeCreatedResponseSchema.parse(r.data);
});

const { hasError } = useErrorWithTimeout(error, 3000);

async function createRecipe(event: SubmitEventPromise) {
  const { valid: formValid } = await event;
  if (formValid) {
    await execute({
      method: 'post',
      url: `${apiUrl}/recipes/`,
      data: recipe.value,
      headers: {
        authorization: 'bearer create:recipe'
      }
    });

    if (!error.value && result.value) {
      router.push({ name: 'RecipeDetails', params: { id: result.value.id } });
    }
  }
}
</script>

<style scoped></style>
