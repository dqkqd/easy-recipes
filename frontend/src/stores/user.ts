import { useAuthStore } from '@/stores/auth';
import { defineStore } from 'pinia';
import { computed } from 'vue';

export const useUserStore = defineStore('use-user-store', () => {
  const auth = useAuthStore();
  const permissions = computed<any[]>(() => {
    if (
      auth.isLoggedIn &&
      auth.payload &&
      auth.payload.permissions &&
      auth.payload.permissions.length
    ) {
      return auth.payload.permissions;
    }
    return [];
  });

  const canCreateRecipe = computed(() => permissions.value.includes('create:recipe'));
  const canUpdateRecipe = computed(() => permissions.value.includes('update:recipe'));
  const canDeleteRecipe = computed(() => permissions.value.includes('delete:recipe'));
  const canCreateIngredient = computed(() => permissions.value.includes('create:ingredient'));
  const canUpdateIngredient = computed(() => permissions.value.includes('update:ingredient'));
  const canDeleteIngredient = computed(() => permissions.value.includes('delete:ingredient'));

  return {
    canCreateRecipe,
    canUpdateRecipe,
    canDeleteRecipe,
    canCreateIngredient,
    canUpdateIngredient,
    canDeleteIngredient
  };
});
