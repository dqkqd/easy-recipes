import RecipeDetails from '@/components/RecipeDetails.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json').as('recipe');
});

describe('Render', () => {
  afterEach(function () {
    cy.getTestSelector('recipe-details-name')
      .should('have.text', this.recipe.name)

      .getTestSelector('recipe-details-image')
      .find('img')
      .should('have.attr', 'src', this.recipe.image_uri)

      .getTestSelector('recipe-details-description')
      .should('have.text', this.recipe.description);
  });

  it('No authentication', function () {
    cy.signJWT(false).then(() => {
      cy.mount(() => h(RecipeDetails, { recipe: this.recipe }))

        .getTestSelector('recipe-details-update-button')
        .should('not.exist')

        .getTestSelector('recipe-details-delete-button')
        .should('not.exist');
    });
  });

  it('Update authentication', function () {
    cy.signJWT(true, ['update:recipe']).then(() => {
      cy.mount(() => h(RecipeDetails, { recipe: this.recipe }))

        .getTestSelector('recipe-details-update-button')
        .should('be.visible')

        .getTestSelector('recipe-details-delete-button')
        .should('not.exist');
    });
  });

  it('Delete authentication', function () {
    cy.signJWT(true, ['delete:recipe']).then(() => {
      cy.mount(() => h(RecipeDetails, { recipe: this.recipe }))

        .getTestSelector('recipe-details-update-button')
        .should('not.exist')

        .getTestSelector('recipe-details-delete-button')
        .should('be.visible');
    });
  });

  it('Update and delete authentication', function () {
    cy.signJWT(true, ['update:recipe', 'delete:recipe']).then(() => {
      cy.mount(() => h(RecipeDetails, { recipe: this.recipe }))

        .getTestSelector('recipe-details-update-button')
        .should('be.visible')

        .getTestSelector('recipe-details-delete-button')
        .should('be.visible');
    });
  });
});

describe('Update recipe', () => {
  beforeEach(function () {
    cy.signJWT(true, ['update:recipe']).then(() => {
      cy.mount(() => h(RecipeDetails, { recipe: this.recipe }));
    });

    cy.getTestSelector('recipe-details-update-dialog')
      .should('not.exist')
      .getTestSelector('recipe-details-update-button')
      .click()
      .getTestSelector('recipe-details-update-dialog')
      .should('be.visible');

    cy.fixture('recipes/details/2.json')
      .as('secondRecipe')
      .then((secondRecipe) => {
        cy.intercept(
          { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}` },
          { ...this.recipe, ...secondRecipe }
        );

        cy.getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .clear()
          .type(secondRecipe.name)
          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-description')
          .find('textarea')
          .clear()
          .type(secondRecipe.description)
          .getTestSelector('form-image-input-url')
          .find('input')
          .clear()
          .type(secondRecipe.image_uri);
      });
  });

  describe('Success', () => {
    afterEach(function () {
      cy.getTestSelector('recipe-details-name')
        .should('have.text', this.secondRecipe.name)

        .getTestSelector('recipe-details-image')
        .find('img')
        .should('have.attr', 'src', this.secondRecipe.image_uri)

        .getTestSelector('recipe-details-description')
        .should('have.text', this.secondRecipe.description);
    });

    it('Update change recipe details', function () {
      cy.getTestSelector('card-recipe-update-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click();
    });

    it('After updating recipe close update dialog', () => {
      cy.getTestSelector('card-recipe-update-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()

        .getTestSelector('recipe-details-update-dialog')
        .should('not.exist');
    });

    it('After updating recipe show success dialog', () => {
      cy.getTestSelector('card-recipe-update-updated-dialog')
        .should('not.exist')
        .getTestSelector('card-recipe-update-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()

        .getTestSelector('card-recipe-update-updated-dialog')
        .should('be.visible')
        .getTestSelector('card-recipe-update-updated-dialog')
        .should('not.exist');
    });
  });

  describe('Failed', () => {
    afterEach(function () {
      cy.getTestSelector('card-recipe-update-updated-dialog')
        .should('not.exist')

        .getTestSelector('recipe-details-name')
        .should('have.text', this.recipe.name)

        .getTestSelector('recipe-details-image')
        .find('img')
        .should('have.attr', 'src', this.recipe.image_uri)

        .getTestSelector('recipe-details-description')
        .should('have.text', this.recipe.description);
    });

    it('Failed update recipe should not change anything', function () {
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}` },
        { forceNetworkError: true }
      );

      cy.getTestSelector('card-recipe-update-error-dialog')
        .should('not.exist')
        .getTestSelector('card-recipe-update-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()

        .getTestSelector('card-recipe-update-error-dialog');
    });
  });
});

describe('Delete recipe', () => {
  beforeEach(function () {
    cy.signJWT(true, ['delete:recipe']).then(() => {
      cy.mount(() => h(RecipeDetails, { recipe: this.recipe }));
    });

    cy.spy(router, 'push').withArgs({ name: 'RecipeView' }).as('redirectedToRecipeVIew');

    cy.getTestSelector('recipe-details-delete-dialog')
      .should('not.exist')

      .getTestSelector('recipe-details-delete-button')
      .click()

      .getTestSelector('recipe-details-delete-dialog')
      .should('be.visible');
  });

  it('Success', function () {
    cy.intercept(
      { method: 'delete', url: `${apiUrl}/recipes/${this.recipe.id}` },
      { id: this.recipe.id }
    );
    cy.getTestSelector('card-warning-accept-button')
      .click()
      .get('@redirectedToRecipeVIew')
      .should('have.been.called');
  });

  it('Failed', function () {
    cy.intercept(
      { method: 'delete', url: `${apiUrl}/recipes/${this.recipe.id}` },
      { forceNetworkError: true }
    );

    cy.getTestSelector('card-warning-accept-button')
      .click()

      .get('@redirectedToRecipeVIew')
      .should('not.have.been.called')
      .getTestSelector('recipe-details-delete-dialog')
      .should('not.exist');
  });

  it('Cancel', () => {
    cy.getTestSelector('card-warning-cancel-button')
      .click()
      .getTestSelector('recipe-details-delete-dialog')
      .should('not.exist');
  });
});

it('Show number of people liked if there are any');
it('Do not show number of people liked if there are none');
