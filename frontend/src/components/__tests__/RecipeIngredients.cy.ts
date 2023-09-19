import RecipeIngredients from '@/components/RecipeIngredients.vue';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import { h } from 'vue';

describe('Render', () => {
  it('Render with ingredients exist', () => {
    cy.signJWT(false).then(() => {
      cy.fixture('recipes/details/1.json').then((recipe) => {
        cy.mount(() => h(RecipeIngredients, { recipe }));
      });
    });

    for (let id = 1; id <= RECIPE_INGREDIENT_PER_PAGE; ++id) {
      cy.getTestSelector(`recipe-ingredients-pagination-${id}`).should('be.visible');
    }

    cy.getTestSelector('recipe-ingredients-title')
      .should('have.text', 'This recipe is made using these ingredients')
      .getTestSelector('recipe-ingredients-pagination')
      .should('be.visible')

      .getTestSelector('recipe-ingredients-pagination-pagination')
      .should('be.visible')
      .getTestSelector('recipe-ingredients-pagination-error-dialog')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-pagination-loading-dialog')
      .should('not.exist')
      .getTestSelector('recipe-ingredients-pagination-pagination')
      .should('be.visible');
  });

  it('Render without ingredients', () => {
    cy.signJWT(false).then(() => {
      cy.fixture('recipes/details/2.json').then((recipe) => {
        cy.mount(() => h(RecipeIngredients, { recipe }));
      });
    });

    cy.getTestSelector('recipe-ingredients-title')
      .should('have.text', 'This recipe is made without any ingredients')
      .getTestSelector('recipe-ingredients-pagination')
      .should('not.exist');
  });

  describe('Permission', () => {
    it('Have update permission', () => {
      cy.signJWT(true, ['update:recipe']).then(() => {
        cy.fixture('recipes/details/1.json').then((recipe) => {
          cy.mount(() => h(RecipeIngredients, { recipe }));
        });
      });

      cy.getTestSelector('recipe-ingredients-dialog-button')
        .should('be.visible')
        .should('have.text', 'Add more ingredients');
    });

    it('No authorized', () => {
      cy.signJWT(false).then(() => {
        cy.fixture('recipes/details/1.json').then((recipe) => {
          cy.mount(() => h(RecipeIngredients, { recipe }));
        });
      });

      cy.getTestSelector('recipe-ingredients-dialog-button').should('not.exist');
    });

    it('Does not have update permission', () => {
      cy.signJWT(true, ['update:ingredient']).then(() => {
        cy.fixture('recipes/details/1.json').then((recipe) => {
          cy.mount(() => h(RecipeIngredients, { recipe }));
        });
      });

      cy.getTestSelector('recipe-ingredients-dialog-button').should('not.exist');
    });
  });
});

describe('Pagination', () => {
  it('Move to second page', () => {
    cy.signJWT(true, ['update:ingredient']).then(() => {
      cy.fixture('recipes/details/1.json').then((recipe) => {
        cy.mount(() => h(RecipeIngredients, { recipe }));
      });
    });

    cy.getTestSelector('recipe-ingredients-pagination-10')
      .should('not.exist')

      .getTestSelector('recipe-ingredients-pagination')
      .findTestSelector('recipe-ingredients-pagination-pagination')
      .find('button[aria-label="Next page"]')
      .click()

      .getTestSelector('recipe-ingredients-pagination-10')
      .should('be.visible');
  });
});

it('Updated ingredients should be changed in pagination pages');
it('Updated ingredients should be changed in select dialog');
