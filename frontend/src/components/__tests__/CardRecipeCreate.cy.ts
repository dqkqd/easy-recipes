import CardRecipeCreate from '@/components/CardRecipeCreate.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import axios from 'axios';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(CardRecipeCreate))
      .getTestSelector('card-recipe-create-title')
      .should('have.text', 'Add new recipe')
      .getTestSelector('card-recipe-create-form-recipe')
      .should('be.visible')
      .getTestSelector('card-recipe-create-error-dialog')
      .should('not.exist');
  });
});

describe('Submit', () => {
  beforeEach(() => {
    cy.spy(router, 'push')
      .withArgs({ name: 'RecipeInfo', params: { id: 1 } })
      .as('redirectedToRecipeInfo');
  });

  describe('Success', () => {
    beforeEach(() => {
      cy.intercept({ method: 'post', url: `${apiUrl}/recipes/` }, { id: 1 });
      cy.fixture('recipes/create/1.json')
        .as('validRecipe')
        .then((recipe) => {
          cy.mount(() => h(CardRecipeCreate))
            .getTestSelector('card-recipe-create-form-recipe')
            .findTestSelector('base-form-name')
            .type(recipe.name)
            .getTestSelector('card-recipe-create-form-recipe')
            .findTestSelector('base-form-description')
            .type(recipe.description);
        });
    });

    afterEach(() => {
      cy.get('@redirectedToRecipeInfo').should('have.been.called');
    });

    it('No image selected', function () {
      const recipe = this.validRecipe;
      recipe.image_uri = null;

      cy.signJWT(true, ['create:recipe']).then((token) => {
        cy.spy(axios, 'request')
          .withArgs({
            method: 'post',
            url: `${apiUrl}/recipes/`,
            data: recipe,
            headers: {
              authorization: `Bearer ${token}`
            }
          })
          .as('requestToBackEnd');
      });

      cy.getTestSelector('card-recipe-create-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image url', function () {
      cy.signJWT(true, ['create:recipe']).then((token) => {
        cy.spy(axios, 'request')
          .withArgs({
            method: 'post',
            url: `${apiUrl}/recipes/`,
            data: this.validRecipe,
            headers: {
              authorization: `Bearer ${token}`
            }
          })
          .as('requestToBackEnd');
      });

      cy.getTestSelector('form-image-input-url')
        .type(this.validRecipe.image_uri)
        .getTestSelector('card-recipe-create-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image file', function () {
      cy.fixture('images/recipe.png', 'base64').then((img) => {
        const recipe = this.validRecipe;
        recipe.image_uri = img;

        cy.signJWT(true, ['create:recipe']).then((token) => {
          cy.spy(axios, 'request')
            .withArgs({
              method: 'post',
              url: `${apiUrl}/recipes/`,
              data: recipe,
              headers: {
                authorization: `Bearer ${token}`
              }
            })
            .as('requestToBackEnd');
        });
      });

      cy.getTestSelector('form-image-input-file')
        .find('input')
        .selectFile('cypress/fixtures/images/recipe.png')
        .getTestSelector('card-recipe-create-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Loading', () => {
      cy.signJWT(true, ['create:recipe']).then(() => {
        cy.get('.v-progress-circular')
          .should('not.exist')
          .getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-description')
          .find('textarea')
          .should('not.be.disabled')
          .getTestSelector('form-image-input-file')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('form-image-input-url')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-submit-button')
          .should('not.be.disabled')

          .getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-submit-button')
          .click()

          .get('.v-progress-circular')
          .should('be.visible')
          .getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .should('be.disabled')
          .getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-description')
          .find('textarea')
          .should('be.disabled')
          .getTestSelector('form-image-input-file')
          .find('input')
          .should('be.disabled')
          .getTestSelector('form-image-input-url')
          .find('input')
          .should('be.disabled');

        cy.once('fail', (err) => {
          expect(err.message).to.include('`cy.click()` failed because this element');
          expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
        });
        cy.getTestSelector('card-recipe-create-form-recipe')
          .findTestSelector('base-form-submit-button')
          .click({ timeout: 100 });
      });
    });
  });

  describe('Failed', () => {
    beforeEach(() => {
      cy.spy(axios, 'request').as('requestToBackEnd');
    });

    afterEach(() => {
      cy.get('@redirectedToRecipeInfo').should('not.have.been.called');
    });

    describe('Invalid response', () => {
      afterEach(() => {
        cy.get('@requestToBackEnd').should('have.been.called');
      });

      it('Network error', () => {
        cy.intercept({ method: 'post', url: `${apiUrl}/recipes/` }, { forceNetworkError: true });
        cy.signJWT(true, ['create:recipe']).then(() => {
          cy.mount(() => h(CardRecipeCreate))
            .getTestSelector('card-recipe-create-form-recipe')
            .findTestSelector('base-form-name')
            .find('input')
            .type('My first recipe')

            .getTestSelector('card-recipe-create-error-dialog')
            .should('not.exist')
            .getTestSelector('card-recipe-create-form-recipe')
            .findTestSelector('base-form-submit-button')
            .click()

            .getTestSelector('card-recipe-create-error-dialog')
            .should('be.visible')
            .wait(2000)
            .getTestSelector('card-recipe-create-error-dialog')
            .should('not.exist');
        });
      });
    });
  });
});
