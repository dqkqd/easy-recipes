<template>
  <VLayout>
    <MainAppBar />
    <VMain class="d-flex align-center justify-center"> </VMain>
  </VLayout>
</template>

<script setup lang="ts">
import MainAppBar from '@/components/MainAppBar.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { IngredientSchema, type Ingredient } from '@/schema/ingredient';
import { onMounted } from 'vue';

const props = defineProps<{ id: number | string }>();

const { result, isLoading, execute } = useAxios<Ingredient>((r) => {
  return IngredientSchema.parse(r.data);
});

onMounted(async () => {
  await execute({
    method: 'get',
    url: `${apiUrl}/ingredients/${props.id}`
  });
});
</script>

<style scoped></style>
