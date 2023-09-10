import RecipeDetails from '@/components/recipes/RecipeDetails.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import { RecipeSchema } from '@/schema/recipe';
import axios from 'axios';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json').as('validRecipeDetails');
});

it('Render properly', function () {
  const recipe = RecipeSchema.parse(this.validRecipeDetails);
  cy.mount(() => h(RecipeDetails, { recipe: recipe }))

    .get('[data-test=recipe-details-name]')
    .should('have.text', recipe.name)

    .get('[data-test=recipe-details-image] img')
    .should('have.attr', 'src', recipe.image_uri)

    .get('[data-test=recipe-details-description]')
    .should('have.text', recipe.description)

    .get('[data-test=recipe-details-like]')
    .should('be.visible')

    // TODO(khanhdq): authorization
    .get('[data-test=recipe-details-update-button]')
    .should('be.visible')

    .get('[data-test=recipe-details-delete-button]')
    .should('be.visible')

    .get('[data-test=recipe-detail-deleted-dialog]')
    .should('not.exist')

    .get('[data-test=recipe-detail-deleting-dialog]')
    .should('not.exist');
});

describe('Delete', () => {
  it('Cancel deletion should not delete recipe', function () {
    const recipe = RecipeSchema.parse(this.validRecipeDetails);
    cy.mount(() => h(RecipeDetails, { recipe: recipe }))

      .get('[data-test=recipe-details-delete-button]')
      .click()

      .get('[data-test=card-warning-cancel-button]')
      .should('be.visible')

      .get('[data-test=card-warning-cancel-button]')
      .click();
  });

  it('Accept deletion should delete recipe', function () {
    const recipe = RecipeSchema.parse(this.validRecipeDetails);
    cy.intercept({ method: 'delete', url: `${apiUrl}/recipes/${recipe.id}` }, { id: recipe.id }).as(
      'deleteRecipe'
    );
    cy.spy(axios, 'request')
      .withArgs({
        method: 'delete',
        url: `${apiUrl}/recipes/${recipe.id}`,
        headers: {
          authorization: 'bearer delete:recipe'
        }
      })
      .as('requestToBackEnd');
    cy.spy(router, 'push').withArgs({ name: 'RecipeView' }).as('redirectedToRecipeVIew');

    cy.mount(() => h(RecipeDetails, { recipe: recipe }))
      .get('[data-test=recipe-details-delete-button]')
      .click()
      .get('[data-test=card-warning-accept-button]')
      .should('be.visible')
      .get('[data-test=card-warning-accept-button]')
      .click()

      .get('@requestToBackEnd')
      .should('be.calledOnce')

      .get('[data-test="recipe-details-deleting-dialog"]')
      .should('be.visible')

      .get('[data-test="recipe-details-deleted-dialog"]')
      .should('be.visible')
      .should('contain.text', 'Recipe deleted')
      .should('contain.text', 'You will be redirected shortly...')

      .wait(2000)
      .get('@redirectedToRecipeVIew')
      .should('be.calledOnce');
  });

  it('Show error if recipe can not be deleted', function () {
    const recipe = RecipeSchema.parse(this.validRecipeDetails);
    cy.intercept(
      { method: 'delete', url: `${apiUrl}/recipes/${recipe.id}` },

      { forceNetworkError: true }
    ).as('deleteRecipe');
    cy.spy(axios, 'request')
      .withArgs({
        method: 'delete',
        url: `${apiUrl}/recipes/${recipe.id}`,
        headers: {
          authorization: 'bearer delete:recipe'
        }
      })
      .as('requestToBackEnd');
    cy.spy(router, 'push').withArgs({ name: 'RecipeView' }).as('redirectedToRecipeVIew');

    cy.mount(() => h(RecipeDetails, { recipe: recipe }))
      .get('[data-test=recipe-details-delete-button]')
      .click()
      .get('[data-test=card-warning-accept-button]')
      .should('be.visible')
      .get('[data-test=card-warning-accept-button]')
      .click()

      .get('@requestToBackEnd')
      .should('be.calledOnce')

      .get('[data-test="recipe-details-deleting-dialog"]')
      .should('be.visible')

      .get('[data-test="recipe-details-delete-error-dialog"]')
      .should('be.visible')
      .should('contain.text', 'Can not delete recipe')
      .should('contain.text', 'Please try again later')

      .get('[data-test="recipe-details-deleted-dialog"]')
      .should('not.exist');
  });
});

it('Show number of people liked if there are any', () => {});
it('Do not show number of people liked if there are none', () => {});
it('Clicking edit button open edit form', () => {});
