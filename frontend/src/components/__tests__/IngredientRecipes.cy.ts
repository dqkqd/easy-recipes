import IngredientRecipes from '@/components/IngredientRecipes.vue';
import { INGREDIENT_RECIPE_PER_PAGE } from '@/utils';
import { h } from 'vue';

describe('Render', () => {
  it('Render with recipes exist', () => {
    cy.fixture('ingredients/details/1.json').then((ingredient) => {
      cy.mount(() => h(IngredientRecipes, { ingredient }));
    });

    for (let id = 1; id <= INGREDIENT_RECIPE_PER_PAGE; ++id) {
      cy.getTestSelector(`ingredient-recipes-pagination-${id}`).should('be.visible');
    }

    cy.getTestSelector('ingredient-recipes-title')
      .should('have.text', 'This ingredient is used in 10 recipes')
      .getTestSelector('ingredient-recipes-pagination')
      .should('be.visible')

      .getTestSelector('ingredient-recipes-pagination-pagination')
      .should('be.visible')
      .getTestSelector('ingredient-recipes-pagination-error-dialog')
      .should('not.exist')
      .getTestSelector('ingredient-recipes-pagination-loading-dialog')
      .should('not.exist')
      .getTestSelector('ingredient-recipes-pagination-pagination')
      .should('be.visible');
  });

  it('Render with one recipe', () => {
    cy.fixture('ingredients/details/3.json').then((ingredient) => {
      cy.mount(() => h(IngredientRecipes, { ingredient }));
    });

    cy.getTestSelector('ingredient-recipes-title')
      .should('have.text', 'This ingredient is used in 1 recipe')
      .getTestSelector('ingredient-recipes-pagination')
      .should('be.visible');
  });

  it('Render without recipes', () => {
    cy.fixture('ingredients/details/2.json').then((ingredient) => {
      cy.mount(() => h(IngredientRecipes, { ingredient }));
    });

    cy.getTestSelector('ingredient-recipes-title')
      .should('have.text', "This ingredient hasn't been used in any recipes")
      .getTestSelector('ingredient-recipes-pagination')
      .should('not.exist');
  });
});

describe('Pagination', () => {
  it.only('Move to second page', () => {
    cy.fixture('ingredients/details/1.json').then((ingredient) => {
      cy.mount(() => h(IngredientRecipes, { ingredient }));
    });

    cy.getTestSelector('ingredient-recipes-pagination-10')
      .should('not.exist')

      .getTestSelector('ingredient-recipes-pagination')
      .findTestSelector('ingredient-recipes-pagination-pagination')
      .find('button[aria-label="Next page"]')
      .click()

      .getTestSelector('ingredient-recipes-pagination-10')
      .should('be.visible');
  });
});
