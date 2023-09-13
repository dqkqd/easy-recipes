import RecipeDetails from '@/components/RecipeDetails.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json')
    .as('recipe')
    .then((recipe) => {
      cy.mount(() => h(RecipeDetails, { recipe: recipe }));
    });
});

it('Render properly', function () {
  cy.get('[data-test=recipe-details-name]')
    .should('have.text', this.recipe.name)

    .get('[data-test=recipe-details-image] img')
    .should('have.attr', 'src', this.recipe.image_uri)

    .get('[data-test=recipe-details-description]')
    .should('have.text', this.recipe.description)

    .get('[data-test=recipe-details-like]')
    .should('be.visible')

    // TODO(khanhdq): authorization
    .get('[data-test=recipe-details-update-button]')
    .should('be.visible')

    .get('[data-test=recipe-details-delete-button]')
    .should('be.visible');
});

describe('Update recipe', () => {
  beforeEach(function () {
    cy.get('[data-test=recipe-details-update-dialog]')
      .should('not.exist')
      .get('[data-test=recipe-details-update-button]')
      .click()
      .get('[data-test=recipe-details-update-dialog]')
      .should('be.visible');

    cy.fixture('recipes/details/2.json')
      .as('secondRecipe')
      .then((secondRecipe) => {
        cy.intercept(
          { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}` },
          { ...this.recipe, ...secondRecipe }
        );

        cy.get('[data-test=form-recipe-name] input')
          .clear()
          .type(secondRecipe.name)
          .get('[data-test=form-recipe-description] textarea')
          .clear()
          .type(secondRecipe.description)
          .get('[data-test=form-image-input-url] input')
          .clear()
          .type(secondRecipe.image_uri);
      });
  });

  describe('Success', () => {
    afterEach(function () {
      cy.get('[data-test=recipe-details-name]')
        .should('have.text', this.secondRecipe.name)

        .get('[data-test=recipe-details-image] img')
        .should('have.attr', 'src', this.secondRecipe.image_uri)

        .get('[data-test=recipe-details-description]')
        .should('have.text', this.secondRecipe.description);
    });

    it('Update change recipe details', function () {
      cy.get('[data-test=form-recipe-submit-button]').click();
    });

    it('After updating recipe close update dialog', () => {
      cy.get('[data-test=form-recipe-submit-button]')
        .click()

        .get('[data-test=recipe-details-update-dialog')
        .should('not.exist');
    });

    it('After updating recipe show success dialog', () => {
      cy.get('[data-test=card-recipe-update-updated-dialog]')
        .should('not.exist')
        .get('[data-test=form-recipe-submit-button]')
        .click()

        .get('[data-test=card-recipe-update-updated-dialog]')
        .should('be.visible')
        .get('[data-test=card-recipe-update-updated-dialog]')
        .should('not.exist');
    });
  });

  describe('Failed', () => {
    afterEach(function () {
      cy.get('[data-test=card-recipe-update-updated-dialog]')
        .should('not.exist')

        .get('[data-test=recipe-details-name]')
        .should('have.text', this.recipe.name)

        .get('[data-test=recipe-details-image] img')
        .should('have.attr', 'src', this.recipe.image_uri)

        .get('[data-test=recipe-details-description]')
        .should('have.text', this.recipe.description);
    });

    it('Failed update recipe should not change anything', function () {
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}` },
        { forceNetworkError: true }
      );

      cy.get('[data-test=card-recipe-update-error-dialog]')
        .should('not.exist')
        .get('[data-test=form-recipe-submit-button]')
        .click()

        .get('[data-test=card-recipe-update-error-dialog]');
    });
  });
});

describe('Delete recipe', () => {
  beforeEach(function () {
    cy.spy(router, 'push').withArgs({ name: 'RecipeView' }).as('redirectedToRecipeVIew');

    cy.get('[data-test=recipe-details-delete-dialog]')
      .should('not.exist')

      .get('[data-test=recipe-details-delete-button]')
      .click()

      .get('[data-test=recipe-details-delete-dialog]')
      .should('be.visible');
  });

  it('Success', function () {
    cy.intercept(
      { method: 'delete', url: `${apiUrl}/recipes/${this.recipe.id}` },
      { id: this.recipe.id }
    );
    cy.get('[data-test=card-warning-accept-button]')
      .click()
      .get('@redirectedToRecipeVIew')
      .should('have.been.called');
  });

  it('Failed', function () {
    cy.intercept(
      { method: 'delete', url: `${apiUrl}/recipes/${this.recipe.id}` },
      { forceNetworkError: true }
    );

    cy.get('[data-test=card-warning-accept-button]')
      .click()

      .get('@redirectedToRecipeVIew')
      .should('not.have.been.called')
      .get('[data-test=recipe-details-delete-dialog]')
      .should('not.exist');
  });

  it('Cancel', () => {
    cy.get('[data-test=card-warning-cancel-button]')
      .click()
      .get('[data-test=recipe-details-delete-dialog]')
      .should('not.exist');
  });
});

it('Show number of people liked if there are any');
it('Do not show number of people liked if there are none');
