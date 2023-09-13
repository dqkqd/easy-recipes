import HomeView from '@/views/HomeView.vue';
import IngredientInfo from '@/views/IngredientInfo.vue';
import IngredientView from '@/views/IngredientView.vue';
import RecipeInfo from '@/views/RecipeInfo.vue';
import RecipeView from '@/views/RecipeView.vue';
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
      path: '/recipes/',
      name: 'RecipeView',
      component: RecipeView
    },
    {
      path: '/ingredients/',
      name: 'IngredientView',
      component: IngredientView
    },
    {
      path: '/recipes/:id(\\d+)',
      name: 'RecipeInfo',
      component: RecipeInfo,
      props: true
    },
    {
      path: '/ingredients/:id(\\d+)',
      name: 'IngredientInfo',
      component: IngredientInfo,
      props: true
    }
  ]
});

export default router;
