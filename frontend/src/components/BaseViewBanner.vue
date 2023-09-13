<template>
  <VImg
    :src="bannerImage"
    :max-height="220"
    gradient="to left, rgba(0,0,0,.1), rgba(0,0,0,.7)"
    cover
    data-test="base-view-banner-image"
  >
    <VRow no-gutters class="py-10" justify="center" align-content="center" align="center">
      <VCol cols="9" align-self="center">
        <div
          class="text-h2 mx-16 font-weight-black text-white me-auto"
          data-test="base-view-banner-title"
        >
          {{ bannerTitle }}
        </div>
      </VCol>

      <VCol v-if="buttonLabel" cols="3" align-self="center">
        <VDialog v-model="dialog" scrollable width="auto" data-test="base-view-banner-dialog">
          <template v-slot:activator="{ props }">
            <VBtn
              color="black"
              v-bind="props"
              :text="buttonLabel"
              class="text-h5 font-weight-black"
              size="x-large"
              data-test="base-view-banner-button"
            />
          </template>

          <slot name="button" />
        </VDialog>
      </VCol>
    </VRow>
  </VImg>
</template>

<script setup lang="ts">
import { ref } from 'vue';
defineProps<{
  bannerImage: string;
  bannerTitle: string;
  buttonLabel?: string;
}>();

const dialog = ref(false);
</script>

<style scoped></style>
