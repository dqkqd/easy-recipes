<template>
  <VHover v-slot="hover">
    <VCard
      :width="130"
      :elevation="!selected && hover && hover.isHovering ? 12 : 2"
      @click="$emit('toggleSelect')"
      data-test="recipe-ingredients-dialog-select-card"
      v-bind="hover && hover.props"
      :class="{ 'ingredient-on-hover': !selected && hover && hover.isHovering, selected: selected }"
    >
      <VTooltip
        activator="parent"
        location="bottom"
        data-test="recipe-ingredients-dialog-select-tooltip-name"
        >{{ props.ingredientName }}</VTooltip
      >

      <VImg
        :src="imageSrc"
        @error="onError"
        lazy-src="/ingredient-cover.jpg"
        :height="100"
        :width="130"
        cover
        data-test="recipe-ingredients-dialog-select-card-image"
      >
        <VIcon
          v-if="selected"
          icon="mdi-check-circle"
          color="blue"
          :size="35"
          data-test="recipe-ingredients-dialog-select-selected-icon"
        />
      </VImg>
      <VCardTitle
        class="text-center font-weight-bold unselectable"
        data-test="recipe-ingredients-dialog-select-card-name"
      >
        {{ ingredientName }}
      </VCardTitle>
    </VCard>
  </VHover>
</template>

<script setup lang="ts">
import { useImage } from '@/composables';
import { stripText } from '@/utils';
import { computed } from 'vue';

const props = defineProps<{
  ingredientName: string;
  ingredientImage: string | null;
  selected: boolean;
}>();

defineEmits<{
  (e: 'toggleSelect'): void;
}>();

const ingredientName = computed(() => stripText(props.ingredientName, 10));

const { imageSrc, onError } = useImage(props.ingredientImage);
</script>

<style scoped>
.ingredient-on-hover {
  color: #40a02b;
}

.unselectable {
  user-select: none;
}

.selected {
  opacity: 0.7;
}
</style>
