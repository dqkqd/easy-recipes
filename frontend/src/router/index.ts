import HomeView from '@/views/HomeView.vue';
import IngredientView from '@/views/ingredient/IngredientView.vue';
import RecipeDetails from '@/views/recipe/RecipeDetails.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ingredients/',
      name: 'IngredientView',
      component: IngredientView
    },
    {
      path: '/recipes/:id(\\d+)',
      name: 'RecipeDetails',
      component: RecipeDetails,
      props: true
    }
  ]
});

export default router;
