<template>
  <VDialog width="auto" v-model="dialog">
    <VAlert prominent :rounded="0" justify="center" type="error" class="px-16 py-5 text-center">
      <VAlertTitle v-if="title" class="text-h5" data-test="dialog-error-title">{{
        title
      }}</VAlertTitle>
      <div v-if="content" data-test="dialog-error-content">{{ content }}</div>
    </VAlert>
  </VDialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  modelValue: boolean;
  title?: string;
  content?: string;
}>();

const emit = defineEmits<{
  (e: 'cancel'): void;
  (e: 'update:modelValue', value: boolean): void;
}>();

const dialog = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  }
});
</script>

<style scoped></style>
