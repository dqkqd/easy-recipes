import RecipeViewPagination from '@/components/RecipeViewPagination.vue';
import { apiUrl } from '@/env';
import axios from 'axios';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/pages/1.json').then((firstPageRecipes) => {
    cy.intercept({ method: 'get', url: `${apiUrl}/recipes/` }, firstPageRecipes);
  });
});

describe('Render', () => {
  it('Render properly', () => {
    cy.spy(axios, 'request')
      .withArgs({
        method: 'get',
        url: `${apiUrl}/recipes/`
      })
      .as('onMountedRequest');

    cy.mount(() => h(RecipeViewPagination));

    for (let id = 1; id <= 5; ++id) {
      cy.getTestSelector(`recipe-view-pagination-${id}`).should('be.visible');
    }

    cy.getTestSelector('recipe-view-pagination-pagination')
      .should('be.visible')

      .getTestSelector('recipe-view-pagination-error-dialog')
      .should('not.exist')
      .getTestSelector('recipe-view-pagination-loading-dialog')
      .should('not.exist')

      // < 1 2 3 4 5 ... 7 > (total 9 lis)
      .getTestSelector('recipe-view-pagination-pagination')
      .find('li')
      .should('have.length', 9)

      .get('@onMountedRequest')
      .should('have.been.calledOnce');
  });
});

describe('Pagination', () => {
  it('Move to second page', () => {
    cy.fixture('recipes/pages/2.json').then((secondPageRecipes) => {
      cy.intercept({ method: 'get', url: `${apiUrl}/recipes/?page=2` }, secondPageRecipes);
    });

    cy.spy(axios, 'request')
      .withArgs({
        method: 'get',
        url: `${apiUrl}/recipes/?page=2`
      })
      .as('pageTwoRecipesRequest');

    cy.mount(() => h(RecipeViewPagination))
      .getTestSelector('recipe-view-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });
    cy.get('@pageTwoRecipesRequest').should('have.been.calledOnce');

    Cypress.on('uncaught:exception', () => {
      return false;
    });
  });
});

describe('Error', () => {
  it('Show error dialog when unable to load recipe', () => {
    cy.intercept({ method: 'get', url: `${apiUrl}/recipes/` }, { forceNetworkError: true });
    cy.mount(() => h(RecipeViewPagination))
      .getTestSelector('recipe-view-pagination-error-dialog')
      .should('be.visible')
      .should('contain.text', 'Unable to load recipes')
      .should('contain.text', 'Please try again later...');
  });
});
