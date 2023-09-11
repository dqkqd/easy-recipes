<template>
  <VDialog persistent width="auto" v-model="dialog">
    <VProgressCircular color="blue" :size="80" indeterminate />
  </VDialog>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  modelValue: boolean;
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
