<template>
  <VRow justify="center">
    <VDialog v-model="dialog" width="auto">
      <template v-slot:activator="{ props }">
        <VBtn :icon="icon" v-bind="props" data-test="delete-button" />
      </template>
      <CardWarning
        :title="title"
        accept-label="Delete"
        cancel-label="Cancel"
        @accept="accept"
        @cancel="cancel"
        data-test="delete-button-dialog"
      />
    </VDialog>
  </VRow>
</template>

<script setup lang="ts">
import CardWarning from '@/components/cards/CardWarning.vue';
import { ref } from 'vue';
withDefaults(
  defineProps<{
    icon?: string;
    title?: string;
  }>(),
  {
    icon: 'mdi-delete'
  }
);

const emit = defineEmits<{
  (e: 'accept'): void;
}>();

const dialog = ref(false);

function cancel() {
  dialog.value = false;
}

function accept() {
  emit('accept');
  dialog.value = false;
}
</script>

<style scoped></style>
