<template>
  <VFileInput
    variant="solo-filled"
    v-model="imageFiles"
    clearable
    :disabled="!!imageUri"
    :accept="supportedImages.join(',')"
    label="Upload your image here, or use url"
    :hint="hint"
    show-size
    prepend-icon=""
    append-inner-icon="mdi-camera"
    data-test="form-image-input-file"
  />

  <VTextField
    variant="solo-filled"
    v-model="imageUri"
    clearable
    :disabled="!!imageFiles.length"
    :hint="hint"
    label="Image URL"
    :rules="[validateURL]"
    data-test="form-image-input-url"
  />
  <VImg :src="imageSrc" @error="onError" :height="400" data-test="form-image-input-image" />
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import { defaultImage } from '@/env';
import { supportedImages } from '@/utils';
import { validateURL } from '@/validators';
import { computed, ref, watch } from 'vue';

const props = withDefaults(
  defineProps<{
    modelValue: string | null;
    hint?: string;
  }>(),
  {
    hint: ''
  }
);

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void;
}>();

const image = computed({
  get() {
    return props.modelValue;
  },
  set(value: string | null) {
    emit('update:modelValue', value);
  }
});

const imageUri = ref('');
const imageFiles = ref<File[]>([]);
const { imageSrc, onError } = useImage(imageUri, imageFiles);

watch(imageSrc, () => {
  if (imageSrc.value === defaultImage) {
    image.value = null;
  } else {
    image.value = imageSrc.value;
  }
});
</script>

<style scoped></style>
