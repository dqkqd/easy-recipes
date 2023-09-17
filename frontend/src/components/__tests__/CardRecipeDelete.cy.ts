import CardRecipeDelete from '@/components/CardRecipeDelete.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import axios from 'axios';
import { h } from 'vue';

beforeEach(() => {
  cy.mount(() => h(CardRecipeDelete, { id: 1, onCancel: cy.spy().as('onCancel') }));
});

describe('Render', () => {
  it('Render properly', () => {
    cy.getTestSelector('card-recipe-delete-warning')
      .should('be.visible')

      .getTestSelector('card-recipe-delete-loading-dialog')
      .should('not.exist')

      .getTestSelector('card-recipe-delete-error-dialog')
      .should('not.exist')

      .getTestSelector('card-recipe-delete-deleted-dialog')
      .should('not.exist');
  });
});

describe('Cancel', () => {
  it('Cancel should emit cancel event', () => {
    cy.getTestSelector('card-warning-cancel-button')
      .click()
      .get('@onCancel')
      .should('have.been.calledOnce');
  });
});

describe('Delete', () => {
  beforeEach(() => {
    cy.signJWT(true, ['delete:recipe']).then((token) => {
      cy.spy(axios, 'request')
        .withArgs({
          method: 'delete',
          url: `${apiUrl}/recipes/1`,
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('requestToBackEnd');
    });

    cy.spy(router, 'push').withArgs({ name: 'RecipeView' }).as('redirectedToRecipeVIew');
  });

  it('Success', () => {
    cy.intercept({ method: 'delete', url: `${apiUrl}/recipes/1` }, { id: 1 });

    cy.getTestSelector('card-warning-accept-button')
      .click()

      .get('@requestToBackEnd')
      .should('have.been.calledOnce')
      .getTestSelector('card-recipe-delete-error-dialog')
      .should('not.exist')
      .getTestSelector('card-recipe-delete-deleted-dialog')
      .should('be.visible')
      .should('contain.text', 'Recipe deleted')
      .should('contain.text', 'You will be redirected shortly...')

      .wait(1500)
      .get('@redirectedToRecipeVIew')
      .should('have.been.called');
  });

  it('Failed', () => {
    cy.intercept({ method: 'delete', url: `${apiUrl}/recipes/1` }, { forceNetworkError: true });

    cy.getTestSelector('card-warning-accept-button')
      .click()

      .get('@requestToBackEnd')
      .should('have.been.calledOnce')

      .getTestSelector('card-recipe-delete-error-dialog')
      .should('be.visible')
      .should('contain.text', 'Can not delete recipe')
      .should('contain.text', 'Please try again later')

      .get('@redirectedToRecipeVIew')
      .should('not.have.been.called')

      .get('@onCancel')
      .should('have.been.calledOnce');
  });

  it('Loading', () => {
    cy.intercept({ method: 'delete', url: `${apiUrl}/recipes/1` }, { delay: 1000 });

    cy.getTestSelector('card-warning-accept-button')
      .click()

      .get('@requestToBackEnd')
      .should('have.been.calledOnce')

      .getTestSelector('card-recipe-delete-loading-dialog')
      .should('be.visible');
  });
});
