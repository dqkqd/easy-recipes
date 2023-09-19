import RecipeIngredientsDialog from '@/components/RecipeIngredientsDialog.vue';
import { apiUrl } from '@/env';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import axios from 'axios';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() =>
      h(RecipeIngredientsDialog, {
        recipeId: 1,
        selectedIngredientIds: [1, 2, 3]
      })
    )
      .getTestSelector('recipe-ingredients-dialog-button')
      .should('have.text', 'Add more ingredients')
      .getTestSelector('recipe-ingredients-dialog-updating')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-dialog-updated-error')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-dialog-updated-success')
      .should('not.exist');
  });
});

describe('Add ingredients button', () => {
  beforeEach(() => {
    const query = {
      per_page: `${RECIPE_INGREDIENT_PER_PAGE}`
    };

    cy.fixture('ingredients/pages/1.json')
      .as('ingredients')
      .then((ingredients) => {
        cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/*`, query }, ingredients);
      });

    const params = new URLSearchParams(query);

    const request = cy.spy(axios, 'request').as('request');

    request
      .withArgs({
        method: 'get',
        url: `${apiUrl}/ingredients/`,
        params
      })
      .as('getIngredientRequest');

    cy.mount(() =>
      h(RecipeIngredientsDialog, {
        recipeId: 1,
        selectedIngredientIds: [1, 2, 3],
        onUpdated: cy.spy().as('onUpdated')
      })
    );
  });

  it('Open dialog when clicking button', () => {
    cy.getTestSelector('recipe-ingredients-dialog-select-pagination')
      .should('not.exist')

      .getTestSelector('recipe-ingredients-dialog-button')
      .click()

      .getTestSelector('recipe-ingredients-dialog-select-pagination')
      .should('be.visible');
  });

  it('No thing happen when clicking submit without editting', () => {
    cy.getTestSelector('recipe-ingredients-dialog-button')
      .click()
      .getTestSelector(`recipe-ingredients-dialog-select-card-1`)
      .click()
      .click()
      .getTestSelector(`recipe-ingredients-dialog-select-card-4`)
      .click()
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click()

      .getTestSelector('recipe-ingredients-dialog-updating')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-dialog-updated-error')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-dialog-updated-success')
      .should('not.exist')

      .get('@onUpdated')
      .should('not.have.been.called');
  });

  it('Change selected ingredients should emit out list of ingredients', function () {
    const ingredientResponses = [...this.ingredients.ingredients.slice(0, 4)].map((v) => {
      delete v.recipes;
      return v;
    });

    cy.fixture('recipes/details/1.json').then((recipe) => {
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/1/ingredients/` },
        { ...recipe, ingredients: ingredientResponses }
      );
    });
    cy.signJWT(true, ['update:recipe']).then((token) => {
      this.request
        .withArgs({
          method: 'patch',
          url: `${apiUrl}/recipes/1/ingredients/`,
          data: {
            ingredients: [1, 2, 3, 4]
          },
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('updateRecipeIngredients');
    });

    cy.getTestSelector('recipe-ingredients-dialog-button')
      .click()
      .getTestSelector(`recipe-ingredients-dialog-select-card-4`)
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click()

      .getTestSelector('recipe-ingredients-dialog-updating')
      .should('be.visible')
      .getTestSelector('recipe-ingredients-dialog-updated-success')
      .should('be.visible')

      .getTestSelector('recipe-ingredients-dialog-updating')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-dialog-updated-success')
      .should('not.exist')

      .get('@updateRecipeIngredients')
      .should('have.been.called')
      .get('@onUpdated')
      .should('have.been.calledWith', ingredientResponses);
  });

  it('Should emit empty ingredients if none selected', function () {
    cy.fixture('recipes/details/1.json').then((recipe) => {
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/1/ingredients/` },
        { ...recipe, ingredients: [] }
      );
    });
    cy.signJWT(true, ['update:recipe']).then((token) => {
      this.request
        .withArgs({
          method: 'patch',
          url: `${apiUrl}/recipes/1/ingredients/`,
          data: {
            ingredients: []
          },
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('updateRecipeIngredients');
    });

    cy.getTestSelector('recipe-ingredients-dialog-button')
      .click()

      .getTestSelector('recipe-ingredients-dialog-select-card-1')
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-card-2')
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-card-3')
      .click()

      .getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click()

      .getTestSelector('recipe-ingredients-dialog-updating')
      .should('be.visible')
      .getTestSelector('recipe-ingredients-dialog-updated-success')
      .should('be.visible')

      .getTestSelector('recipe-ingredients-dialog-updating')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-dialog-updated-success')
      .should('not.exist')

      .get('@updateRecipeIngredients')
      .should('have.been.called')
      .get('@onUpdated')
      .should('have.been.calledWith', []);
  });

  it('Should show error dialog when failed and make it disapear', function () {
    cy.intercept(
      { method: 'patch', url: `${apiUrl}/recipes/1/ingredients/` },
      { forceNetworkError: true }
    );

    cy.signJWT(true, ['update:recipe']).then((token) => {
      this.request
        .withArgs({
          method: 'patch',
          url: `${apiUrl}/recipes/1/ingredients/`,
          data: {
            ingredients: [1, 2, 3, 4]
          },
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('updateRecipeIngredients');
    });

    cy.getTestSelector('recipe-ingredients-dialog-button')
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-card-4')
      .click()

      .getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click()

      .getTestSelector('recipe-ingredients-dialog-updated-error')
      .should('be.visible')
      .getTestSelector('recipe-ingredients-dialog-updated-error')
      .should('not.exist')

      .get('@updateRecipeIngredients')
      .should('have.been.called')
      .get('@onUpdated')
      .should('not.have.been.called');
  });
});
