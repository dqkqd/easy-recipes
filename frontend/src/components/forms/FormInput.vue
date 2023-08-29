<template>
  <div>
    <label>{{ props.label }}:</label>
    <input :placeholder="props.placeholder" v-model="value" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  label: string;
  placeholder: string;
  modelValue: string | null;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void;
}>();

const value = computed({
  get() {
    return props.modelValue;
  },

  set(value) {
    emit('update:modelValue', value);
  }
});
</script>

<style scoped></style>
