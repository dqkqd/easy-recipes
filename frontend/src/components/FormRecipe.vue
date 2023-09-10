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
        <FormImageInput
          v-model="image"
          :loading="loading"
          :image="recipe?.image_uri"
          hint="Please provide the best image to describe your recipe"
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
import FormImageInput from '@/components/FormImageInput.vue';
import type { Recipe } from '@/schema/recipe';
import { required } from '@/validators';
import { computed, ref } from 'vue';
import type { SubmitEventPromise } from 'vuetify';

const props = withDefaults(
  defineProps<{
    loading?: boolean;
    recipe?: Recipe;
  }>(),
  {
    loading: false
  }
);

const emit = defineEmits<{
  (e: 'submit', name: string, image: string | null, description: string): void;
}>();

const name = ref(props.recipe?.name ?? '');
const description = ref(props.recipe?.description ?? '');
const image = ref(null);

const validating = ref(false);
const loading = computed(() => props.loading || validating.value);

async function submit(event: SubmitEventPromise) {
  validating.value = true;
  const formValidationResult = await event;
  validating.value = false;

  if (formValidationResult.valid) {
    emit('submit', name.value, image.value, description.value);
  }
}
</script>

<style scoped></style>
