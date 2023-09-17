import IngredientViewPagination from '@/components/IngredientViewPagination.vue';
import { apiUrl } from '@/env';
import axios from 'axios';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('ingredients/pages/1.json').then((firstPageIngredients) => {
    cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/` }, firstPageIngredients);
  });
});

describe('Render', () => {
  it('Render properly', () => {
    cy.spy(axios, 'request')
      .withArgs({
        method: 'get',
        url: `${apiUrl}/ingredients/`
      })
      .as('onMountedRequest');

    cy.mount(() => h(IngredientViewPagination));

    for (let id = 1; id <= 5; ++id) {
      cy.getTestSelector(`ingredient-view-pagination-${id}`).should('be.visible');
    }

    cy.getTestSelector('ingredient-view-pagination-pagination')
      .should('be.visible')

      .getTestSelector('ingredient-view-pagination-error-dialog')
      .should('not.exist')
      .getTestSelector('ingredient-view-pagination-loading-dialog')
      .should('not.exist')

      // < 1 2 3 4 5 ... 7 > (total 9 lis)
      .getTestSelector('ingredient-view-pagination-pagination')
      .find('li')
      .should('have.length', 9)

      .get('@onMountedRequest')
      .should('have.been.calledOnce');
  });
});

describe('Pagination', () => {
  it('Move to second page', () => {
    cy.fixture('ingredients/pages/2.json').then((secondPageIngredients) => {
      cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/?page=2` }, secondPageIngredients);
    });

    cy.spy(axios, 'request')
      .withArgs({
        method: 'get',
        url: `${apiUrl}/ingredients/?page=2`
      })
      .as('pageTwoIngredientsRequest');

    cy.mount(() => h(IngredientViewPagination))
      .getTestSelector('ingredient-view-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });
    cy.get('@pageTwoIngredientsRequest').should('have.been.calledOnce');

    Cypress.on('uncaught:exception', () => {
      return false;
    });
  });
});

describe('Error', () => {
  it('Show error dialog when unable to load ingredients', () => {
    cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/` }, { forceNetworkError: true });
    cy.mount(() => h(IngredientViewPagination))
      .getTestSelector('ingredient-view-pagination-error-dialog')
      .should('be.visible')
      .should('contain.text', 'Unable to load ingredients')
      .should('contain.text', 'Please try again later...');
  });
});
