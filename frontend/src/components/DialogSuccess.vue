<template>
  <VDialog persistent width="auto" v-model="dialog" data-test="card-recipe-delete-deleted-dialog">
    <VAlert prominent :rounded="0" justify="center" type="success" class="px-16 py-5 text-center">
      <VAlertTitle class="text-h5">Recipe deleted</VAlertTitle>
      <div>You will be redirected shortly...</div>
    </VAlert>
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
