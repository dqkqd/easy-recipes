import { apiUrl } from '@/env';
import IngredientView from '@/views/IngredientView.vue';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('ingredients/pages/1.json').then((firstPageIngredients) => {
    cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/` }, firstPageIngredients);
  });
});

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(IngredientView))
      .get('[data-test=ingredient-view-banner]')
      .should('be.visible')
      .get('[data-test=ingredient-view-pagination]')
      .should('be.visible')
      .get('[data-test=ingredient-view-footer]')
      .should('be.visible');
  });
});
