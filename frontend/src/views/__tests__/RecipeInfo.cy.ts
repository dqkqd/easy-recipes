import { apiUrl } from '@/env';
import RecipeInfo from '@/views/RecipeInfo.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render without error', () => {
    cy.fixture('recipes/details/1.json').then((recipe) => {
      cy.intercept({ method: 'get', url: `${apiUrl}/recipes/${recipe.id}` }, recipe);
      cy.mount(() => h(RecipeInfo, { id: recipe.id }))
        .getTestSelector('recipe-info-dialog-loading')
        .should('be.visible')
        .getTestSelector('recipe-info-dialog-error')
        .should('not.exist')

        .getTestSelector('recipe-info-recipe-details')
        .should('be.visible')
        .getTestSelector('recipe-info-recipe-ingredients')
        .should('be.visible')
        .getTestSelector('recipe-info-footer')
        .should('be.visible');
    });
  });

  it.only('Render with error', () => {
    cy.fixture('recipes/details/1.json').then((recipe) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/recipes/${recipe.id}` },
        { forceNetworkError: true }
      );
      cy.mount(() => h(RecipeInfo, { id: recipe.id }))
        .getTestSelector('recipe-info-dialog-error')
        .should('be.visible')
        .getTestSelector('recipe-info-recipe-details')
        .should('not.exist')
        .getTestSelector('recipe-info-recipe-ingredients')
        .should('not.exist')
        .getTestSelector('recipe-info-footer')
        .should('be.visible');
    });
  });
});
