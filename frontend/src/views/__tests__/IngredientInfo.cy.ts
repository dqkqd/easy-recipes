import { apiUrl } from '@/env';
import IngredientInfo from '@/views/IngredientInfo.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render without error', () => {
    cy.fixture('ingredients/details/1.json').then((ingredient) => {
      cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/${ingredient.id}` }, ingredient);
      cy.mount(() => h(IngredientInfo, { id: ingredient.id }))
        .getTestSelector('ingredient-info-dialog-error')
        .should('not.exist')

        .getTestSelector('ingredient-info-ingredient-details')
        .should('be.visible')
        .getTestSelector('ingredient-info-ingredient-recipes')
        .should('be.visible')
        .getTestSelector('ingredient-info-footer')
        .should('be.visible');
    });
  });

  it('Render with error', () => {
    cy.fixture('ingredients/details/1.json').then((ingredient) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/ingredients/${ingredient.id}` },
        { forceNetworkError: true }
      );
      cy.mount(() => h(IngredientInfo, { id: ingredient.id }))
        .getTestSelector('ingredient-info-dialog-error')
        .should('be.visible')
        .getTestSelector('ingredient-info-recipe-details')
        .should('not.exist')
        .getTestSelector('ingredient-info-ingredient-recipes')
        .should('not.exist')
        .getTestSelector('ingredient-info-footer')
        .should('be.visible');
    });
  });
});
