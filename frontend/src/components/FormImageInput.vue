<template>
  <VFileInput
    variant="solo-filled"
    v-model="imageFiles"
    clearable
    :disabled="!!imageUri || loading"
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
    :disabled="!!imageFiles.length || loading"
    :hint="hint"
    label="Image URL"
    :rules="[validateURL]"
    data-test="form-image-input-url"
  />
  <VImg :src="imageSrc" @error="onError" :height="400" data-test="form-image-input-image" />
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import { supportedImages } from '@/utils';
import { validateURL } from '@/validators';
import { computed, onMounted, ref, watch } from 'vue';

const props = withDefaults(
  defineProps<{
    modelValue: string | null;
    hint?: string;
    loading: boolean;
    image?: string | null;
  }>(),
  {
    hint: '',
    loading: false,
    image: null
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
const { imageSrc, onError, realImage } = useImage(props.image, imageUri, imageFiles);

watch(imageSrc, () => {
  image.value = realImage.value;
});

onMounted(() => {
  image.value = realImage.value;
});
</script>

<style scoped></style>
