<template>
  <DialogLoading v-model="isLoading" data-test="card-recipe-delete-loading-dialog" />

  <DialogError
    v-model="hasError"
    title="Can not delete recipe"
    content="Please try again later..."
    data-test="card-recipe-delete-error-dialog"
  />

  <DialogSuccess
    v-model="deleted"
    title="Recipe deleted"
    content="You will be redirected shortly..."
    data-test="card-recipe-delete-deleted-dialog"
  />

  <CardWarning
    title="Are you sure you want to delete your recipe?"
    accept-label="Delete"
    cancel-label="Cancel"
    @accept="deleteRecipe"
    @cancel="$emit('cancel')"
    data-test="card-recipe-delete-warning"
  />
</template>

<script setup lang="ts">
import CardWarning from '@/components/CardWarning.vue';
import DialogError from '@/components/DialogError.vue';
import DialogLoading from '@/components/DialogLoading.vue';
import DialogSuccess from '@/components/DialogSuccess.vue';
import { useAxios } from '@/composables';
import { apiUrl } from '@/env';
import { RecipeDeletedResponseSchema, type RecipeDeletedResponse } from '@/schema/recipe';
import { useAuth0 } from '@auth0/auth0-vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps<{
  id: number;
}>();

const emit = defineEmits<{
  (e: 'cancel'): void;
}>();

const router = useRouter();

const deleted = ref(false);
const hasError = ref(false);

const { result, error, isLoading, execute } = useAxios<RecipeDeletedResponse>((r) => {
  return RecipeDeletedResponseSchema.parse(r.data);
});

const auth = useAuth0();

async function deleteRecipe() {
  const token = await auth.getAccessTokenSilently();
  await execute({
    method: 'delete',
    url: `${apiUrl}/recipes/${props.id}`,
    headers: {
      authorization: `Bearer ${token}`
    }
  });

  if (!error.value && result.value) {
    deleted.value = true;
    setTimeout(() => {
      router.push({ name: 'RecipeView' });
    }, 1500);
  } else {
    hasError.value = true;
    setTimeout(() => {
      emit('cancel');
    }, 2000);
  }
}
</script>

<style scoped></style>
