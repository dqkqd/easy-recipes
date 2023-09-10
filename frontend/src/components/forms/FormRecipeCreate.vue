<template>
  <VForm class="pt-8" :disabled="loading" fast-fail @submit.prevent="submit">
    <VRow>
      <VCol>
        <VTextField
          variant="solo-filled"
          v-model="name"
          clearable
          label="Name *"
          required
          :rules="[required('Name')]"
          data-test="form-recipe-create-name"
        />

        <VTextarea
          variant="solo-filled"
          v-model="description"
          rows="19"
          clearable
          label="Description"
          hint="Please provide the best description to describe your recipe"
          density="compact"
          data-test="form-recipe-create-description"
        />
      </VCol>

      <VCol>
        <FormImageInput
          v-model="image"
          hint="Please provide the best image to describe your recipe"
          data-test="form-recipe-create-form-image-input"
        />
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
          data-test="form-recipe-create-submit-button"
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
          data-test="form-recipe-create-cancel-button"
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
import FormImageInput from '@/components/forms/FormImageInput.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import {
  RecipeCreateSchema,
  RecipeCreatedResponseSchema,
  type RecipeCreatedResponse
} from '@/schema/recipe';
import { replaceBase64Prefix } from '@/utils';
import { required } from '@/validators';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import type { SubmitEventPromise } from 'vuetify';

const name = ref('');
const image = ref(null);
const description = ref('');

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
      image_uri: image.value,
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
