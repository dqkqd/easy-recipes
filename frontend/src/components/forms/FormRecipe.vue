<template>
  <VForm class="pt-8" :disabled="loading" fast-fail @submit.prevent="submit">
    <VRow>
      <VCol>
        <VTextField
          variant="solo-filled"
          v-model="name"
          clearable
          validate-on="submit"
          label="Name *"
          required
          :rules="[required('Name')]"
          data-test="form-recipe-name"
        />

        <VTextarea
          variant="solo-filled"
          v-model="description"
          rows="19"
          clearable
          label="Description"
          hint="Please provide the best description to describe your recipe"
          density="compact"
          data-test="form-recipe-description"
        />
      </VCol>

      <VCol>
        <VFileInput
          variant="solo-filled"
          v-model="imageFiles"
          clearable
          :disabled="!!imageUri"
          :accept="supportedImages.join(',')"
          label="Upload your image here, or use url"
          hint="Please provide the best image to describe your recipe"
          show-size
          prepend-icon=""
          append-inner-icon="mdi-camera"
        />

        <VTextField
          variant="solo-filled"
          v-model="imageUri"
          clearable
          :disabled="!!imageFiles.length"
          label="Image URL"
          hint="Please provide the best image to describe your recipe"
          validate-on="submit"
          :rules="[validateURL]"
          data-test="form-recipe-image-uri"
        />
        <VImg :src="imageSrc" @error="onError" :height="400" />
      </VCol>
    </VRow>

    <VRow class="px-2">
      <VCol>
        <VBtn
          type="submit"
          :loading="loading"
          block
          color="#04a5e5"
          elevation="5"
          class="text-h5 text-center"
          size="x-large"
          data-test="form-recipe-submit-button"
          text="Submit"
        />
      </VCol>
      <VCol>
        <VBtn
          :disabled="loading"
          block
          color="#9ca0b0"
          elevation="5"
          class="text-h5 text-center"
          size="x-large"
          data-test="form-recipe-cancel-button"
          text="Cancel"
          @click="$emit('cancel')"
        />
      </VCol>
    </VRow>
  </VForm>

  <VDialog
    :width="500"
    v-model="hasError"
    transition="fade-transition"
    data-test="card-recipe-create-error-dialog"
  >
    <VAlert color="red-darken-2" prominent :rounded="0" type="error" title="Error adding recipe" />
  </VDialog>
</template>

<script setup lang="ts">
import { useAxios, useErrorWithTimeout, useImage } from '@/composables';
import { apiUrl, defaultImage } from '@/env';
import {
  RecipeCreateSchema,
  RecipeCreatedResponseSchema,
  type RecipeCreatedResponse
} from '@/schema/recipe';
import { replaceBase64Prefix, supportedImages } from '@/utils';
import { required, validateURL } from '@/validators';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import type { SubmitEventPromise } from 'vuetify';

const name = ref('');
const description = ref('');
const imageUri = ref('');

const imageFiles = ref<File[]>([]);
const { imageSrc, onError } = useImage(imageUri, imageFiles);

const { result, isLoading, error, execute } = useAxios<RecipeCreatedResponse>(
  (r) => {
    return RecipeCreatedResponseSchema.parse(r.data);
  },
  (data) => {
    const parsedData = RecipeCreateSchema.parse(data);
    parsedData.image_uri = replaceBase64Prefix(parsedData.image_uri);
    return parsedData;
  }
);

const { hasError } = useErrorWithTimeout(error, 2000);

const validating = ref(false);
const loading = computed(() => isLoading.value || validating.value);

const router = useRouter();

async function submit(event: SubmitEventPromise) {
  validating.value = true;
  const formValidationResult = await event;
  validating.value = false;

  if (!formValidationResult.valid) {
    return;
  }

  await execute({
    method: 'post',
    url: `${apiUrl}/recipes/`,
    data: {
      name: name.value,
      image_uri: imageSrc.value === defaultImage ? null : imageSrc.value,
      description: description.value
    },
    headers: {
      authorization: 'bearer create:recipe'
    }
  });

  if (!error.value && result.value) {
    router.push({ name: 'RecipeInfo', params: { id: result.value.id } });
  }
}
</script>

<style scoped></style>
