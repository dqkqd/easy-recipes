import { apiUrl } from '@/env';
import RecipeView from '@/views/RecipeView.vue';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/pages/1.json').then((firstPageRecipes) => {
    cy.intercept({ method: 'get', url: `${apiUrl}/recipes/` }, firstPageRecipes);
  });
});

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(RecipeView))
      .get('[data-test=recipe-view-banner]')
      .should('be.visible')
      .get('[data-test=recipe-view-pagination]')
      .should('be.visible')
      .get('[data-test=recipe-view-footer]')
      .should('be.visible');
  });
});
