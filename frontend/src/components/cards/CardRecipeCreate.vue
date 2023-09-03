<template>
  <VSheet :width="800">
    <VCard class="px-5 pb-8">
      <VCardTitle
        class="text-center my-8 py-1 font-weight-black text-h4"
        data-test="card-recipe-create-title"
        >Add new recipe</VCardTitle
      >
      <VForm :disabled="loading" fast-fail @submit.prevent="createRecipe">
        <VTextField
          variant="solo-filled"
          v-model="name"
          clearable
          label="Name *"
          required
          :rules="[(v) => !!v || 'Name is required']"
          class="pb-4"
          data-test="card-form-recipe-create-name"
        />

        <VTextField
          variant="solo-filled"
          v-model="image_uri"
          clearable
          label="Image URL *"
          hint="Please provide the best image to describe your recipe"
          :rules="[validateURL]"
          class="pb-4"
          data-test="card-form-recipe-create-image-uri"
        />

        <VTextarea
          variant="underlined"
          v-model="description"
          clearable
          label="Description"
          hint="Please provide the best description to describe your recipe"
          density="compact"
          class="pb-4"
          data-test="card-form-recipe-create-description"
        />

        <VBtn
          type="submit"
          :loading="loading"
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
          <CardError>
            <template v-slot:error-message>Can't add new recipe. Please try again.</template>
          </CardError>
        </VDialog>
      </VForm>
    </VCard>
  </VSheet>
</template>

<script setup lang="ts">
import CardError from '@/components/cards/CardError.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeCreatedResponseSchema, type RecipeCreatedResponse } from '@/schema/recipe';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import type { SubmitEventPromise } from 'vuetify';
import { z } from 'zod';

const name = ref('');
const description = ref('');
const image_uri = ref('');

const loading = ref(false);

function validateURL(url: string) {
  const zodURL = z.string().url();
  const { success } = zodURL.safeParse(url.trim());
  return success || 'Invalid URL';
}

const router = useRouter();
const { result, error, execute } = useAxios<RecipeCreatedResponse>((r) => {
  return RecipeCreatedResponseSchema.parse(r.data);
});

async function createRecipe(event: SubmitEventPromise) {
  loading.value = true;
  const { valid: formValid } = await event;
  if (formValid) {
    await execute({
      method: 'post',
      url: `${apiUrl}/recipes/`,
      data: { name: name.value, description: description.value, image_uri: image_uri.value },
      headers: {
        authorization: 'bearer create:recipe'
      }
    });

    if (!error.value && result.value) {
      router.push({ name: 'RecipeDetails', params: { id: result.value.id } });
    }
  }

  loading.value = false;
}

const hasError = ref(false);
watch(error, () => {
  if (error.value) {
    hasError.value = true;
    setTimeout(() => (hasError.value = false), 3000);
  }
});
</script>

<style scoped></style>
