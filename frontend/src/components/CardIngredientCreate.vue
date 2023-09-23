<template>
  <VSheet :width="800">
    <VCard class="px-5 pb-8">
      <VCardTitle
        class="text-center my-8 py-1 font-weight-black text-h4"
        data-test="card-ingredient-create-title"
        >Add new ingredient</VCardTitle
      >

      <FormIngredient
        :loading="isLoading"
        @submit="createIngredient"
        data-test="card-ingredient-create-form-ingredient"
      />
    </VCard>

    <VDialog
      :width="500"
      v-model="hasError"
      transition="fade-transition"
      data-test="card-ingredient-create-error-dialog"
    >
      <VAlert
        color="red-darken-2"
        prominent
        :rounded="0"
        type="error"
        title="Error adding ingredient"
      />
    </VDialog>
  </VSheet>
</template>

<script setup lang="ts">
import FormIngredient from '@/components/FormIngredient.vue';
import { useAxios, useErrorWithTimeout } from '@/composables';
import { apiUrl } from '@/env';
import {
  IngredientCreateSchema,
  IngredientCreatedResponseSchema,
  type IngredientCreatedResponse
} from '@/schema/ingredient';
import { useAuthStore } from '@/stores/auth';
import { replaceBase64Prefix } from '@/utils';
import { useRouter } from 'vue-router';

const { result, isLoading, error, execute } = useAxios<IngredientCreatedResponse>(
  (r) => {
    return IngredientCreatedResponseSchema.parse(r.data);
  },
  (data) => {
    const parsedData = IngredientCreateSchema.parse(data);
    parsedData.image_uri = replaceBase64Prefix(parsedData.image_uri);
    return parsedData;
  }
);

const { hasError } = useErrorWithTimeout(error, 2000);

const router = useRouter();
const auth = useAuthStore();

async function createIngredient(name: string, image: string | null, description: string) {
  await execute({
    method: 'post',
    url: `${apiUrl}/ingredients/`,
    data: {
      name: name,
      image_uri: image,
      description: description
    },
    headers: {
      authorization: `Bearer ${auth.token}`
    }
  });

  if (!error.value && result.value) {
    router.push({ name: 'IngredientInfo', params: { id: result.value.id } });
  }
}
</script>

<style scoped></style>
