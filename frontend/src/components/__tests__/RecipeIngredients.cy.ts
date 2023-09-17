import RecipeIngredients from '@/components/RecipeIngredients.vue';
import { apiUrl } from '@/env';
import axios from 'axios';
import { h } from 'vue';

describe('Render', () => {
  beforeEach(() => {
    cy.spy(axios, 'request')
      .withArgs({ method: 'get', url: `${apiUrl}/recipes/1/ingredients/` })
      .as('onMountedRequest');
  });

  afterEach(() => {
    cy.get('@onMountedRequest').should('have.been.calledOnce');
  });

  it('Render with ingredients exist', () => {
    cy.fixture('ingredients/pages/1.json').then((firstPageIngredients) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/recipes/1/ingredients/` },
        firstPageIngredients
      );
    });

    cy.mount(() => h(RecipeIngredients, { id: 1 }));

    for (let id = 1; id <= 5; ++id) {
      cy.getTestSelector(`recipe-ingredients-pagination-${id}`).should('be.visible');
    }

    cy.getTestSelector('recipe-ingredients-title')
      .should('have.text', 'This recipe is made using these ingredients')
      .getTestSelector('recipe-ingredients-add-ingredients-button')
      .should('have.text', 'Add more ingredients')
      .getTestSelector('recipe-ingredients-pagination')
      .should('be.visible')

      .getTestSelector('recipe-ingredients-pagination-pagination')
      .should('be.visible')
      .getTestSelector('recipe-ingredients-pagination-error-dialog')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-pagination-loading-dialog')
      .should('not.exist')

      // < 1 2 3 4 5 ... 7 > (total 9 lis)
      .getTestSelector('recipe-ingredients-pagination-pagination')
      .find('li')
      .should('have.length', 9);
  });

  it('Render without ingredients', () => {
    cy.fixture('ingredients/pages/no-ingredients.json').then((firstPageIngredients) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/recipes/1/ingredients/` },
        firstPageIngredients
      );
    });

    cy.mount(() => h(RecipeIngredients, { id: 1 }));
    cy.getTestSelector('recipe-ingredients-title')
      .should('have.text', 'This recipe is made without any ingredients')
      .getTestSelector('recipe-ingredients-add-ingredients-button')
      .should('have.text', 'Add more ingredients')
      .getTestSelector('recipe-ingredients-pagination')
      .should('not.exist');
  });
});

describe('Pagination', () => {
  it('Move to second page', () => {
    cy.fixture('ingredients/pages/1.json').then((firstPageIngredients) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/recipes/1/ingredients/` },
        firstPageIngredients
      );
    });
    cy.fixture('ingredients/pages/2.json').then((secondPageIngredients) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/recipes/1/ingredients/?page=2` },
        secondPageIngredients
      );
    });

    cy.spy(axios, 'request')
      .withArgs({
        method: 'get',
        url: `${apiUrl}/recipes/1/ingredients/?page=2`
      })
      .as('pageTwoIngredientsRequest');

    cy.mount(() => h(RecipeIngredients, { id: 1 }))
      .getTestSelector('recipe-ingredients-loading-dialog')
      .should('be.visible')

      .getTestSelector('recipe-ingredients-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });
    cy.get('@pageTwoIngredientsRequest')
      .should('have.been.calledOnce')
      .getTestSelector('recipe-ingredients-loading-dialog')
      .should('be.visible');

    Cypress.on('uncaught:exception', () => {
      return false;
    });
  });
});

describe('Error', () => {
  it('Show error dialog when unable to load ingredients', () => {
    cy.intercept(
      { method: 'get', url: `${apiUrl}/recipes/1/ingredients/` },
      { forceNetworkError: true }
    );
    cy.mount(() => h(RecipeIngredients))
      .getTestSelector('recipe-ingredients-pagination-error-dialog')
      .should('be.visible')
      .should('contain.text', 'Unable to load ingredients')
      .should('contain.text', 'Please try again later...');
  });
});
