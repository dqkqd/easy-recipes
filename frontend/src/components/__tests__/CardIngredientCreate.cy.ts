import CardIngredientCreate from '@/components/CardIngredientCreate.vue';
import { apiUrl } from '@/env';
import auth0 from '@/plugins/auth0';
import router from '@/router';
import axios from 'axios';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(CardIngredientCreate))
      .get('[data-test=card-ingredient-create-title]')
      .should('have.text', 'Add new ingredient')
      .get('[data-test=card-ingredient-create-form-ingredient]')
      .should('be.visible')
      .get('[data-test=card-ingredient-create-error-dialog]')
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
      cy.stub(auth0, 'getAccessTokenSilently').returns(Cypress.env('menuManagerToken'));
      cy.intercept({ method: 'post', url: `${apiUrl}/ingredients/` }, { id: 1 });
      cy.fixture('ingredients/create/1.json')
        .as('validIngredient')
        .then((ingredient) => {
          cy.mount(() => h(CardIngredientCreate))
            .get('[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-name]')
            .type(ingredient.name)
            .get(
              '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-description]'
            )
            .type(ingredient.description);
        });
    });

    afterEach(() => {
      cy.get('@redirectToIngredientInfo').should('have.been.called');
    });

    it('No image selected', function () {
      const ingredient = this.validIngredient;
      ingredient.image_uri = null;

      cy.spy(axios, 'request')
        .withArgs({
          method: 'post',
          url: `${apiUrl}/ingredients/`,
          data: ingredient,
          headers: {
            authorization: `Bearer ${Cypress.env('menuManagerToken')}`
          }
        })
        .as('requestToBackEnd');

      cy.get(
        '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
      )
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image url', function () {
      cy.spy(axios, 'request')
        .withArgs({
          method: 'post',
          url: `${apiUrl}/ingredients/`,
          data: this.validIngredient,
          headers: {
            authorization: `Bearer ${Cypress.env('menuManagerToken')}`
          }
        })
        .as('requestToBackEnd');

      cy.get('[data-test=form-image-input-url]')
        .type(this.validIngredient.image_uri)
        .get(
          '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
        )
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Input image file', function () {
      cy.fixture('images/ingredient.png', 'base64').then((img) => {
        const ingredient = this.validIngredient;
        ingredient.image_uri = img;
        cy.spy(axios, 'request')
          .withArgs({
            method: 'post',
            url: `${apiUrl}/ingredients/`,
            data: ingredient,
            headers: {
              authorization: `Bearer ${Cypress.env('menuManagerToken')}`
            }
          })
          .as('requestToBackEnd');
      });

      cy.get('[data-test=form-image-input-file] input')
        .selectFile('cypress/fixtures/images/ingredient.png')
        .get(
          '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
        )
        .click()
        .get('@requestToBackEnd')
        .should('have.been.called');
    });

    it('Loading', () => {
      cy.get('.v-progress-circular')
        .should('not.exist')
        .get('[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-name] input')
        .should('not.be.disabled')
        .get(
          '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-description] textarea'
        )
        .should('not.be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('not.be.disabled')
        .get(
          '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
        )
        .should('not.be.disabled')

        .get(
          '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
        )
        .click()

        .get('.v-progress-circular')
        .should('be.visible')
        .get('[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-name] input')
        .should('be.disabled')
        .get(
          '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-description] textarea'
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
        '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
      ).click({ timeout: 100 });
    });
  });

  describe('Failed', () => {
    beforeEach(() => {
      cy.stub(auth0, 'getAccessTokenSilently').returns(Cypress.env('menuManagerToken'));
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
        cy.mount(() => h(CardIngredientCreate))
          .get(
            '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-name] input'
          )
          .type('My first ingredient')

          .get('[data-test=card-ingredient-create-error-dialog]')
          .should('not.exist')
          .get(
            '[data-test=card-ingredient-create-form-ingredient] [data-test=base-form-submit-button]'
          )
          .click()

          .get('[data-test=card-ingredient-create-error-dialog]')
          .should('be.visible')
          .wait(2000)
          .get('[data-test=card-ingredient-create-error-dialog]')
          .should('not.exist');
      });
    });
  });
});
