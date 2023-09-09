import CardRecipeCreate from '@/components/cards/CardRecipeCreate.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import axios from 'axios';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(CardRecipeCreate))
      .get('[data-test=card-recipe-create-title]')
      .should('have.text', 'Add new recipe')
      .get('[data-test=card-recipe-create-form-recipe]')
      .should('be.visible')
      .get('[data-test=card-recipe-create-error-dialog]')
      .should('not.exist');
  });
});

describe('Add recipe', () => {
  beforeEach(function () {
    cy.spy(router, 'push')
      .withArgs({ name: 'RecipeInfo', params: { id: 1 } })
      .as('redirectedToRecipeInfo');

    cy.fixture('recipes/create/1.json').then((validRecipeCreate) => {
      cy.spy(axios, 'request')
        .withArgs({
          method: 'post',
          url: `${apiUrl}/recipes/`,
          data: validRecipeCreate,
          headers: {
            authorization: 'bearer create:recipe'
          }
        })
        .as('requestToBackEnd');

      cy.mount(() => h(CardRecipeCreate))
        .get('[data-test=card-recipe-create-form-recipe] [data-test=form-recipe-name] input')
        .type(validRecipeCreate.name)
        .get('[data-test=card-recipe-create-form-recipe] [data-test=form-recipe-image-uri] input')
        .type(validRecipeCreate.image_uri)
        .get(
          '[data-test=card-recipe-create-form-recipe] [data-test=form-recipe-description] textarea'
        )
        .type(validRecipeCreate.description);
    });
  });

  it('Add valid recipe', function () {
    cy.intercept({ method: 'post', url: `${apiUrl}/recipes/` }, { id: 1 }).as('createRecipe');

    cy.get('[data-test=card-recipe-create-form-recipe] [data-test=form-recipe-submit-button]')
      .click()

      .get('@requestToBackEnd')
      .should('be.called')

      .wait('@createRecipe')

      .get('@redirectedToRecipeInfo')
      .should('be.called');
  });

  it('Add recipe with loading', function () {
    cy.intercept({ method: 'post', url: `${apiUrl}/recipes/` }, { id: 1 }).as('createRecipe');

    cy.get('.v-progress-circular')
      .should('not.exist')

      .get('[data-test=card-recipe-create-form-recipe] [data-test=form-recipe-submit-button]')
      .click()

      .should('exist');
  });

  it('Add recipe with network error', function () {
    cy.intercept({ method: 'post', url: `${apiUrl}/recipes/` }, { forceNetworkError: true }).as(
      'createRecipe'
    );

    cy.get('[data-test=card-recipe-create-form-recipe] [data-test=form-recipe-submit-button]')
      .click()

      .get('@requestToBackEnd')
      .should('be.called')

      .wait('@createRecipe')

      .get('@redirectedToRecipeInfo')
      .should('not.be.called')

      .get('[data-test=card-recipe-create-error-dialog]')
      .should('be.visible')
      .wait(2000)
      .get('[data-test=card-recipe-create-error-dialog]')
      .should('not.exist');
  });
});
