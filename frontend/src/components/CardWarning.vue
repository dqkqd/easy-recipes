<template>
  <VSheet border rounded>
    <div v-if="title" class="text-h5 font-weight-bold ma-4" data-test="card-warning-title">
      {{ title }}
    </div>
    <VDivider />
    <VRow justify="center" class="ma-2">
      <VCol cols="5">
        <VBtn
          block
          class="text-h6 text-black font-weight-bold"
          color="red-accent-2"
          size="large"
          variant="flat"
          @click="$emit('accept')"
          data-test="card-warning-accept-button"
        >
          {{ acceptLabel }}
        </VBtn>
      </VCol>
      <VCol cols="5">
        <VBtn
          block
          class="text-h6 font-weight-bold"
          color="grey-lighten-3"
          size="large"
          variant="flat"
          @click="$emit('cancel')"
          data-test="card-warning-cancel-button"
        >
          {{ cancelLabel }}
        </VBtn>
      </VCol>
    </VRow>
  </VSheet>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string;
    acceptLabel?: string;
    cancelLabel?: string;
  }>(),
  {
    title: '',
    acceptLabel: 'Accept',
    cancelLabel: 'Cancel'
  }
);

defineEmits<{
  (e: 'accept'): void;
  (e: 'cancel'): void;
}>();
</script>

<style scoped></style>
