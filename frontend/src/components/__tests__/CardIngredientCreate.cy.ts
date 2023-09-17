import CardIngredientCreate from '@/components/CardIngredientCreate.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import axios from 'axios';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(CardIngredientCreate))
      .getTestSelector('card-ingredient-create-title')
      .should('have.text', 'Add new ingredient')
      .getTestSelector('card-ingredient-create-form-ingredient')
      .should('be.visible')
      .getTestSelector('card-ingredient-create-error-dialog')
      .should('not.exist');
  });
});

describe('Submit', () => {
  beforeEach(() => {
    cy.spy(router, 'push')
      .withArgs({ name: 'IngredientInfo', params: { id: 1 } })
      .as('redirectToIngredientInfo');
  });

  describe('Success', () => {
    beforeEach(() => {
      cy.intercept({ method: 'post', url: `${apiUrl}/ingredients/` }, { id: 1 });
      cy.fixture('ingredients/create/1.json')
        .as('validIngredient')
        .then((ingredient) => {
          cy.mount(() => h(CardIngredientCreate))
            .getTestSelector('card-ingredient-create-form-ingredient')
            .findTestSelector('base-form-name')
            .type(ingredient.name)
            .getTestSelector('card-ingredient-create-form-ingredient')
            .findTestSelector('base-form-description')
            .type(ingredient.description);
        });
    });

    afterEach(() => {
      cy.get('@redirectToIngredientInfo').should('have.been.called');
    });

    it('No image selected', function () {
      const ingredient = this.validIngredient;
      ingredient.image_uri = null;

      cy.signJWT(true, ['create:ingredient']).then((token) => {
        cy.spy(axios, 'request')
          .withArgs({
            method: 'post',
            url: `${apiUrl}/ingredients/`,
            data: ingredient,
            headers: {
              authorization: `Bearer ${token}`
            }
          })
          .as('requestToBackEnd');
      });

      cy.getTestSelector('card-ingredient-create-form-ingredient')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image url', function () {
      cy.signJWT(true, ['create:ingredient']).then((token) => {
        cy.spy(axios, 'request')
          .withArgs({
            method: 'post',
            url: `${apiUrl}/ingredients/`,
            data: this.validIngredient,
            headers: {
              authorization: `Bearer ${token}`
            }
          })
          .as('requestToBackEnd');
      });

      cy.getTestSelector('form-image-input-url')
        .type(this.validIngredient.image_uri)
        .getTestSelector('card-ingredient-create-form-ingredient')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image file', function () {
      cy.fixture('images/ingredient.png', 'base64').then((img) => {
        const ingredient = this.validIngredient;
        ingredient.image_uri = img;

        cy.signJWT(true, ['create:ingredient']).then((token) => {
          cy.spy(axios, 'request')
            .withArgs({
              method: 'post',
              url: `${apiUrl}/ingredients/`,
              data: ingredient,
              headers: {
                authorization: `Bearer ${token}`
              }
            })
            .as('requestToBackEnd');
        });
      });

      cy.getTestSelector('form-image-input-file')
        .find('input')
        .selectFile('cypress/fixtures/images/ingredient.png')
        .getTestSelector('card-ingredient-create-form-ingredient')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Loading', () => {
      cy.signJWT(true, ['create:ingredient']).then(() => {
        cy.get('.v-progress-circular')
          .should('not.exist')
          .getTestSelector('card-ingredient-create-form-ingredient')
          .findTestSelector('base-form-name')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('card-ingredient-create-form-ingredient')
          .findTestSelector('base-form-description')
          .find('textarea')
          .should('not.be.disabled')
          .getTestSelector('form-image-input-file')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('form-image-input-url')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('card-ingredient-create-form-ingredient')
          .findTestSelector('base-form-submit-button')
          .should('not.be.disabled')

          .getTestSelector('card-ingredient-create-form-ingredient')
          .findTestSelector('base-form-submit-button')
          .click()

          .get('.v-progress-circular')
          .should('be.visible')
          .getTestSelector('card-ingredient-create-form-ingredient')
          .findTestSelector('base-form-name')
          .find('input')
          .should('be.disabled')
          .getTestSelector('card-ingredient-create-form-ingredient')
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
        cy.getTestSelector('card-ingredient-create-form-ingredient')
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
      cy.get('@redirectToIngredientInfo').should('not.have.been.called');
    });

    describe('Invalid response', () => {
      afterEach(() => {
        cy.get('@requestToBackEnd').should('have.been.called');
      });

      it('Network error', () => {
        cy.intercept(
          { method: 'post', url: `${apiUrl}/ingredients/` },
          { forceNetworkError: true }
        );

        cy.signJWT(true, ['create:ingredient']).then(() => {
          cy.mount(() => h(CardIngredientCreate))
            .getTestSelector('card-ingredient-create-form-ingredient')
            .findTestSelector('base-form-name')
            .find('input')
            .type('My first ingredient')

            .getTestSelector('card-ingredient-create-error-dialog')
            .should('not.exist')
            .getTestSelector('card-ingredient-create-form-ingredient')
            .findTestSelector('base-form-submit-button')
            .click()

            .getTestSelector('card-ingredient-create-error-dialog')
            .should('be.visible')
            .wait(2000)
            .getTestSelector('card-ingredient-create-error-dialog')
            .should('not.exist');
        });
      });
    });
  });
});
