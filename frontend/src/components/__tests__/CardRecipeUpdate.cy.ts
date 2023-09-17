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
    cy.get('[data-test=card-recipe-update-title]')
      .should('have.text', 'Update your recipe')
      .get('[data-test=card-recipe-update-form-recipe]')
      .should('be.visible')
      .get('[data-test=card-recipe-update-error-dialog]')
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

        cy.get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-name] input')
          .clear()
          .type(recipe.name)
          .get(
            '[data-test=card-recipe-update-form-recipe] [data-test=base-form-description] textarea'
          )
          .clear()
          .type(recipe.description)
          .get('[data-test=form-image-input-url] input')
          .clear()
          .type(recipe.image_uri)

          .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]')
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

        cy.get('[data-test=form-image-input-file] input')
          .selectFile('cypress/fixtures/images/recipe.png')
          .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]')
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
          .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-name] input')
          .should('not.be.disabled')
          .type('New name')

          .get(
            '[data-test=card-recipe-update-form-recipe] [data-test=base-form-description] textarea'
          )
          .should('not.be.disabled')
          .get('[data-test=form-image-input-file] input')
          .should('not.be.disabled')
          .get('[data-test=form-image-input-url] input')
          .should('not.be.disabled')
          .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]')
          .should('not.be.disabled')

          .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]')
          .click()

          .get('.v-progress-circular')
          .should('be.visible')
          .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-name] input')
          .should('be.disabled')
          .get(
            '[data-test=card-recipe-update-form-recipe] [data-test=base-form-description] textarea'
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
          '[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]'
        ).click({ timeout: 100 });
      });
    });
  });

  describe('Nothing changes', () => {
    beforeEach(() => {
      cy.spy(axios, 'request').as('requestToBackEnd');
    });

    afterEach(() => {
      cy.get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]')
        .click()
        .get('@requestToBackEnd')
        .should('not.have.been.called');
    });

    it('Submit without editting', () => {});

    describe('Editting then rollback', () => {
      it('Name', function () {
        cy.get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-name] input').type(
          `{selectall}{backspace}${this.recipe.name}`
        );
      });

      it('Description', function () {
        cy.get(
          '[data-test=card-recipe-update-form-recipe] [data-test=base-form-description] textarea'
        ).type(`{selectall}{backspace}${this.recipe.description}`);
      });

      it('Image URL', function () {
        cy.get('[data-test=form-image-input-url] input')
          .type(`{selectall}{backspace}${this.recipe.image_uri}`)
          .type('{selectall}{backspace}');
      });

      it('Image file', function () {
        cy.get('[data-test=form-image-input-file] input')
          .selectFile('cypress/fixtures/images/recipe.png')
          .get('[data-test=form-image-input-file] i[role=button]')
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
          cy.get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-name] input')
            .type('{selectall}{backspace}My new recipe')

            .get('[data-test=card-recipe-update-error-dialog]')
            .should('not.exist')
            .get('[data-test=card-recipe-update-form-recipe] [data-test=base-form-submit-button]')
            .click()

            .get('[data-test=card-recipe-update-error-dialog]')
            .should('be.visible')
            .wait(2000)
            .get('[data-test=card-recipe-update-error-dialog]')
            .should('not.exist');
        });
      });
    });
  });
});
