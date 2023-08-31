<template>
  <div>
    <button @click="$emit('close')" data-test="delete-button">{{ props.label }}</button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  label: string;
}>();
</script>

<style scoped></style>
