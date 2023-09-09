<template>
  <VForm :disabled="loading" fast-fail @submit.prevent="submit">
    <VTextField
      variant="solo-filled"
      v-model="name"
      clearable
      label="Name *"
      required
      :rules="[required('Name')]"
      class="pb-4"
      data-test="form-recipe-name"
    />

    <VTextField
      variant="solo-filled"
      v-model="imageUri"
      clearable
      label="Image URL *"
      hint="Please provide the best image to describe your recipe"
      :rules="[validateURL]"
      class="pb-4"
      data-test="form-recipe-image-uri"
    />

    <VTextarea
      variant="underlined"
      v-model="description"
      clearable
      label="Description"
      hint="Please provide the best description to describe your recipe"
      density="compact"
      class="pb-4"
      data-test="form-recipe-description"
    />

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
</template>

<script setup lang="ts">
import { required, validateURL } from '@/validators';
import { computed, ref } from 'vue';
import type { SubmitEventPromise } from 'vuetify';

const imageUri = ref('');
const name = ref('');
const description = ref('');

const props = withDefaults(
  defineProps<{
    loading?: boolean;
  }>(),
  {
    loading: false
  }
);

const emit = defineEmits<{
  (e: 'submit', name: string, imageUri: string, description: string): void;
  (e: 'cancel'): void;
}>();

const validating = ref(false);
async function submit(event: SubmitEventPromise) {
  validating.value = true;
  const result = await event;
  validating.value = false;
  if (result.valid) {
    emit('submit', name.value, imageUri.value, description.value);
  }
}

const loading = computed(() => props.loading || validating.value);
</script>

<style scoped></style>
