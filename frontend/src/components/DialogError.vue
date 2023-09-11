<template>
  <VDialog width="auto" v-model="dialog" data-test="card-recipe-delete-error-dialog">
    <VAlert prominent :rounded="0" justify="center" type="error" class="px-16 py-5 text-center">
      <VAlertTitle class="text-h5">Can not delete recipe</VAlertTitle>
      <div>Please try again later</div>
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
