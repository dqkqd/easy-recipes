<template>
  <VCard class="text-center" color="red-lighten-1" rounded>
    <VCardTitle>
      <VIcon size="x-large" icon="mdi-emoticon-sad-outline" />
      <VCardItem class="font-weight-black text-h5">Oops</VCardItem>
      <VCardText class="text-h6" data-test="card-error-text">
        <slot name="error-message"></slot>
      </VCardText>
    </VCardTitle>
  </VCard>
</template>

<script setup lang="ts"></script>

<style scoped></style>
