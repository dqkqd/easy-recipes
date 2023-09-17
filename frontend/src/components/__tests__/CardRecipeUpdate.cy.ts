import CardRecipeUpdate from '@/components/CardRecipeUpdate.vue';
import { apiUrl } from '@/env';
import axios from 'axios';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json')
    .as('recipe')
    .then((recipe) => {
      cy.mount(() =>
        h(CardRecipeUpdate, {
          recipe: recipe,
          onUpdated: cy.spy().as('onUpdated')
        })
      );
    });
});

describe('Render', () => {
  it('Render properly', () => {
    cy.getTestSelector('card-recipe-update-title')
      .should('have.text', 'Update your recipe')
      .getTestSelector('card-recipe-update-form-recipe')
      .should('be.visible')
      .getTestSelector('card-recipe-update-error-dialog')
      .should('not.exist');
  });
});

describe('Submit', () => {
  describe('Success', () => {
    afterEach(() => {
      cy.get('@requestToBackEnd').should('have.been.called');
    });

    it('Update name, description and image url', function () {
      cy.fixture('recipes/details/2.json').then((secondRecipe) => {
        const recipe = { ...this.recipe };
        recipe.name = secondRecipe.name;
        recipe.image_uri = secondRecipe.image_uri;
        recipe.description = secondRecipe.description;

        cy.intercept({ method: 'patch', url: `${apiUrl}/recipes/${recipe.id}` }, { ...recipe });

        cy.signJWT(true, ['update:recipe']).then((token) => {
          cy.spy(axios, 'request')
            .withArgs({
              method: 'patch',
              url: `${apiUrl}/recipes/${recipe.id}`,
              data: {
                name: recipe.name,
                image_uri: recipe.image_uri,
                description: recipe.description
              },
              headers: {
                authorization: `Bearer ${token}`
              }
            })
            .as('requestToBackEnd');
        });

        cy.getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .clear()
          .type(recipe.name)
          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-description')
          .find('textarea')
          .clear()
          .type(recipe.description)
          .getTestSelector('form-image-input-url')
          .find('input')
          .clear()
          .type(recipe.image_uri)

          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-submit-button')
          .click()

          .get('@onUpdated')
          .should('have.been.calledOnceWith', recipe.name, recipe.image_uri, recipe.description);
      });
    });

    it('Update image file', function () {
      cy.fixture('images/recipe.png', 'base64').then((img) => {
        const recipe = { ...this.recipe };
        recipe.image_uri = img;
        cy.intercept(
          { method: 'patch', url: `${apiUrl}/recipes/${recipe.id}` },
          { ...recipe, image_uri: 'https://picsum.photos/200' }
        );

        cy.signJWT(true, ['update:recipe']).then((token) => {
          cy.spy(axios, 'request')
            .withArgs({
              method: 'patch',
              url: `${apiUrl}/recipes/${recipe.id}`,
              data: {
                name: recipe.name,
                image_uri: recipe.image_uri,
                description: recipe.description
              },
              headers: {
                authorization: `Bearer ${token}`
              }
            })
            .as('requestToBackEnd');
        });

        cy.getTestSelector('form-image-input-file')
          .find('input')
          .selectFile('cypress/fixtures/images/recipe.png')
          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-submit-button')
          .click()
          .get('@onUpdated')
          .should('have.been.calledOnce');
      });
    });

    it('Loading', function () {
      cy.spy(axios, 'request').as('requestToBackEnd');
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}` },
        { ...this.recipe, name: 'New name' }
      );

      cy.signJWT(true, ['update:recipe']).then(() => {
        cy.get('.v-progress-circular')
          .should('not.exist')
          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .should('not.be.disabled')
          .type('New name')

          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-description')
          .find('textarea')
          .should('not.be.disabled')
          .getTestSelector('form-image-input-file')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('form-image-input-url')
          .find('input')
          .should('not.be.disabled')
          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-submit-button')
          .should('not.be.disabled')

          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-submit-button')
          .click()

          .get('.v-progress-circular')
          .should('be.visible')
          .getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .should('be.disabled')
          .getTestSelector('card-recipe-update-form-recipe')
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
        cy.getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-submit-button')
          .click({ timeout: 100 });
      });
    });
  });

  describe('Nothing changes', () => {
    beforeEach(() => {
      cy.spy(axios, 'request').as('requestToBackEnd');
    });

    afterEach(() => {
      cy.getTestSelector('card-recipe-update-form-recipe')
        .findTestSelector('base-form-submit-button')
        .click()
        .get('@requestToBackEnd')
        .should('not.have.been.called');
    });

    it('Submit without editting', () => {});

    describe('Editting then rollback', () => {
      it('Name', function () {
        cy.getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-name')
          .find('input')
          .type(`{selectall}{backspace}${this.recipe.name}`);
      });

      it('Description', function () {
        cy.getTestSelector('card-recipe-update-form-recipe')
          .findTestSelector('base-form-description')
          .find('textarea')
          .type(`{selectall}{backspace}${this.recipe.description}`);
      });

      it('Image URL', function () {
        cy.getTestSelector('form-image-input-url')
          .find('input')
          .type(`{selectall}{backspace}${this.recipe.image_uri}`)
          .type('{selectall}{backspace}');
      });

      it('Image file', function () {
        cy.getTestSelector('form-image-input-file')
          .find('input')
          .selectFile('cypress/fixtures/images/recipe.png')
          .getTestSelector('form-image-input-file')
          .find('i[role=button]')
          .click();
      });
    });
  });

  describe('Failed', () => {
    beforeEach(() => {
      cy.spy(axios, 'request').as('requestToBackEnd');
    });

    describe('Invalid response', () => {
      afterEach(() => {
        cy.get('@requestToBackEnd').should('have.been.called');
      });

      it('Network error', function () {
        cy.intercept(
          { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}` },
          { forceNetworkError: true }
        );

        cy.signJWT(true, ['update:recipe']).then(() => {
          cy.getTestSelector('card-recipe-update-form-recipe')
            .findTestSelector('base-form-name')
            .find('input')
            .type('{selectall}{backspace}My new recipe')

            .getTestSelector('card-recipe-update-error-dialog')
            .should('not.exist')
            .getTestSelector('card-recipe-update-form-recipe')
            .findTestSelector('base-form-submit-button')
            .click()

            .getTestSelector('card-recipe-update-error-dialog')
            .should('be.visible')
            .wait(2000)
            .getTestSelector('card-recipe-update-error-dialog')
            .should('not.exist');
        });
      });
    });
  });
});
