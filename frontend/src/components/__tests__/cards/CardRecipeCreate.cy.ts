import CardRecipeCreate from '@/components/cards/CardRecipeCreate.vue';
import { apiUrl } from '@/env';
import router from '@/router';

it('Render properly', () => {
  cy.mount(CardRecipeCreate);

  cy.get('[data-test="card-recipe-create-title"]').should('have.text', 'Add new recipe');

  cy.get('[data-test="card-form-recipe-create-name"]')
    .find('label')
    .first()
    .should('have.text', 'Name *');

  cy.get('[data-test="card-form-recipe-create-image-uri"]')
    .find('label')
    .first()
    .should('have.text', 'Image URL *');

  cy.get('[data-test="card-form-recipe-create-description"]')
    .find('label')
    .first()
    .should('have.text', 'Description');

  cy.get('[data-test="card-form-recipe-create-submit-button"]').should('have.text', 'ADD');
});

it('Mock create valid recipe', () => {
  cy.mount(CardRecipeCreate);

  cy.spy(router, 'push')
    .withArgs({ name: 'RecipeDetails', params: { id: 1 } })
    .as('redirectedToRecipeDetails');

  cy.intercept({ method: 'POST', url: `${apiUrl}/recipes/` }, { id: 1 }).as('createRecipe');

  cy.get('[data-test="card-form-recipe-create-name"]').find('input').type('My first recipe');
  cy.get('[data-test="card-form-recipe-create-image-uri"]')
    .find('input')
    .type('https://images.unsplash.com/photo-1466637574441-749b8f19452f');

  cy.get('[data-test="card-form-recipe-create-submit-button"]').click();
  cy.wait('@createRecipe');
  cy.get('@redirectedToRecipeDetails').should('be.called');
});
