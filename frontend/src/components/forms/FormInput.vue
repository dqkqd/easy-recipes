<template>
  <div>
    <label>{{ props.label }}:</label>
    <input
      :placeholder="props.label"
      :value="props.modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  label: string;
  modelValue: string | null;
}>();
</script>

<style scoped></style>
