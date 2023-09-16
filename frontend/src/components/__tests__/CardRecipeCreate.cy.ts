import CardRecipeCreate from '@/components/CardRecipeCreate.vue';
import { apiUrl } from '@/env';
import auth0 from '@/plugins/auth0';
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

describe('Submit', () => {
  beforeEach(() => {
    cy.stub(auth0, 'getAccessTokenSilently').returns(Cypress.env('menuManagerToken'));
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
            .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-name]')
            .type(recipe.name)
            .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-description]')
            .type(recipe.description);
        });
    });

    afterEach(() => {
      cy.get('@redirectedToRecipeInfo').should('have.been.called');
    });

    it('No image selected', function () {
      const recipe = this.validRecipe;
      recipe.image_uri = null;

      cy.spy(axios, 'request')
        .withArgs({
          method: 'post',
          url: `${apiUrl}/recipes/`,
          data: recipe,
          headers: {
            authorization: `Bearer ${Cypress.env('menuManagerToken')}`
          }
        })
        .as('requestToBackEnd');

      cy.get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image url', function () {
      cy.spy(axios, 'request')
        .withArgs({
          method: 'post',
          url: `${apiUrl}/recipes/`,
          data: this.validRecipe,
          headers: {
            authorization: `Bearer ${Cypress.env('menuManagerToken')}`
          }
        })
        .as('requestToBackEnd');

      cy.get('[data-test=form-image-input-url]')
        .type(this.validRecipe.image_uri)
        .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image file', function () {
      cy.fixture('images/recipe.png', 'base64').then((img) => {
        const recipe = this.validRecipe;
        recipe.image_uri = img;
        cy.spy(axios, 'request')
          .withArgs({
            method: 'post',
            url: `${apiUrl}/recipes/`,
            data: recipe,
            headers: {
              authorization: `Bearer ${Cypress.env('menuManagerToken')}`
            }
          })
          .as('requestToBackEnd');
      });

      cy.get('[data-test=form-image-input-file] input')
        .selectFile('cypress/fixtures/images/recipe.png')
        .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Loading', () => {
      cy.get('.v-progress-circular')
        .should('not.exist')
        .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-name] input')
        .should('not.be.disabled')
        .get(
          '[data-test=card-recipe-create-form-recipe] [data-test=base-form-description] textarea'
        )
        .should('not.be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('not.be.disabled')
        .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]')
        .should('not.be.disabled')

        .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]')
        .click()

        .get('.v-progress-circular')
        .should('be.visible')
        .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-name] input')
        .should('be.disabled')
        .get(
          '[data-test=card-recipe-create-form-recipe] [data-test=base-form-description] textarea'
        )
        .should('be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('be.disabled');

      cy.once('fail', (err) => {
        expect(err.message).to.include('`cy.click()` failed because this element');
        expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
      });
      cy.get(
        '[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]'
      ).click({ timeout: 100 });
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
        cy.mount(() => h(CardRecipeCreate))
          .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-name] input')
          .type('My first recipe')

          .get('[data-test=card-recipe-create-error-dialog]')
          .should('not.exist')
          .get('[data-test=card-recipe-create-form-recipe] [data-test=base-form-submit-button]')
          .click()

          .get('[data-test=card-recipe-create-error-dialog]')
          .should('be.visible')
          .wait(2000)
          .get('[data-test=card-recipe-create-error-dialog]')
          .should('not.exist');
      });
    });
  });
});
