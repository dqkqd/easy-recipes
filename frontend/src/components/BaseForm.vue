<template>
  <VForm class="pt-8" :disabled="loading" fast-fail @submit.prevent="submit">
    <VRow>
      <VCol>
        <VTextField
          variant="solo-filled"
          v-model="formName"
          clearable
          label="Name *"
          required
          :rules="[required('Name')]"
          data-test="base-form-name"
        />

        <VTextarea
          variant="solo-filled"
          v-model="formDescription"
          rows="19"
          clearable
          label="Description"
          hint="Please provide the best description to describe your recipe"
          density="compact"
          data-test="base-form-description"
        />
      </VCol>

      <VCol>
        <FormImageInput
          v-model="formImage"
          :loading="loading"
          :image="image"
          hint="Please provide the best image to describe your recipe"
        />
      </VCol>
    </VRow>

    <VRow class="px-2">
      <VBtn
        type="submit"
        :loading="loading"
        block
        color="black"
        elevation="5"
        class="text-h5 text-center font-weight-black"
        size="x-large"
        data-test="base-form-submit-button"
        text="Submit"
      />
    </VRow>
  </VForm>
</template>

<script setup lang="ts">
import FormImageInput from '@/components/FormImageInput.vue';
import { required } from '@/validators';
import { computed, ref } from 'vue';
import type { SubmitEventPromise } from 'vuetify';

const props = withDefaults(
  defineProps<{
    loading?: boolean;
    name?: string;
    image?: string | null;
    description?: string | null;
  }>(),
  {
    loading: false
  }
);

const emit = defineEmits<{
  (e: 'submit', name: string, image: string | null, description: string): void;
}>();

const formName = ref(props.name ?? '');
const formDescription = ref(props.description ?? '');
const formImage = ref(null);

const validating = ref(false);
const loading = computed(() => props.loading || validating.value);

async function submit(event: SubmitEventPromise) {
  validating.value = true;
  const formValidationResult = await event;
  validating.value = false;

  if (formValidationResult.valid) {
    emit('submit', formName.value, formImage.value, formDescription.value);
  }
}
</script>

<style scoped></style>
