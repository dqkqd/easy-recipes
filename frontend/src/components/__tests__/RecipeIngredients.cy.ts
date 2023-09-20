import RecipeIngredients from '@/components/RecipeIngredients.vue';
import { apiUrl } from '@/env';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import axios from 'axios';
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

describe('Updating ingredients', () => {
  beforeEach(() => {
    // page 1
    cy.fixture('ingredients/pages/1.json')
      .as('firstPageIngredients')
      .then((ingredients) => {
        cy.intercept(
          {
            method: 'get',
            url: `${apiUrl}/ingredients/*`,
            query: {
              per_page: `${RECIPE_INGREDIENT_PER_PAGE}`
            }
          },
          ingredients
        );
      });

    // page 2
    cy.fixture('ingredients/pages/2.json')
      .as('secondPageIngredients')
      .then((ingredients) => {
        cy.intercept(
          {
            method: 'get',
            url: `${apiUrl}/ingredients/*`,
            query: {
              page: '2',
              per_page: `${RECIPE_INGREDIENT_PER_PAGE}`
            }
          },
          ingredients
        );
      });

    cy.fixture('recipes/details/1.json').as('recipe');
  });

  it('Updated ingredients should be changed in pagination pages', function () {
    const updatedIngredients = [...this.secondPageIngredients.ingredients.slice(0, 4)].map((v) => {
      delete v.recipes;
      return v;
    });

    cy.signJWT(true, ['update:recipe']).then((token) => {
      cy.mount(() => h(RecipeIngredients, { recipe: this.recipe }));
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}/ingredients/` },
        { ...this.recipe, ingredients: updatedIngredients }
      );
      cy.spy(axios, 'request')
        .withArgs({
          method: 'patch',
          url: `${apiUrl}/recipes/${this.recipe.id}/ingredients/`,
          data: {
            ingredients: [6, 7, 8, 9]
          },
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('updateRecipeIngredients');
    });

    cy.getTestSelector('recipe-ingredients-dialog-button').click();
    for (const id of [1, 2, 3, 4, 5]) {
      cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`).click();
    }

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    cy.getTestSelector(`recipe-ingredients-dialog-select-card-10`)
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click()
      .get('@updateRecipeIngredients')
      .should('have.been.called');

    for (const id of [1, 2, 3, 4, 5]) {
      cy.getTestSelector(`recipe-ingredients-pagination-${id}`).should('not.exist');
    }
    for (const id of [6, 7, 8, 9]) {
      cy.getTestSelector(`recipe-ingredients-pagination-${id}`).should('be.visible');
    }
  });

  it('Updated ingredients should be changed in select dialog', function () {
    const updatedIngredients = [...this.firstPageIngredients.ingredients.slice(0, 3)].map((v) => {
      delete v.recipes;
      return v;
    });

    cy.signJWT(true, ['update:recipe']).then((token) => {
      cy.mount(() => h(RecipeIngredients, { recipe: this.recipe }));
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}/ingredients/` },
        { ...this.recipe, ingredients: updatedIngredients }
      );
      cy.spy(axios, 'request')
        .withArgs({
          method: 'patch',
          url: `${apiUrl}/recipes/${this.recipe.id}/ingredients/`,
          data: {
            ingredients: [1, 2, 3]
          },
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('updateRecipeIngredients');
    });

    cy.getTestSelector('recipe-ingredients-dialog-button').click();

    for (const id of [4, 5]) {
      cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`).click();
    }

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    for (const id of [6, 7, 8, 9, 10]) {
      cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`).click();
    }

    cy.getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click()
      .getTestSelector('recipe-ingredients-dialog-button')
      .click();

    for (const id of [4, 5]) {
      cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
        .findTestSelector('recipe-ingredients-dialog-select-card')
        .should('not.have.class', 'selected');
    }

    for (const id of [1, 2, 3]) {
      cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
        .findTestSelector('recipe-ingredients-dialog-select-card')
        .should('have.class', 'selected');
    }
  });

  it('Update ingredients should change pagination page to page one', function () {
    const updatedIngredients = [
      ...this.firstPageIngredients.ingredients,
      ...this.secondPageIngredients.ingredients.slice(0, 4)
    ].map((v) => {
      delete v.recipes;
      return v;
    });

    cy.signJWT(true, ['update:recipe']).then((token) => {
      cy.mount(() => h(RecipeIngredients, { recipe: this.recipe }));
      cy.intercept(
        { method: 'patch', url: `${apiUrl}/recipes/${this.recipe.id}/ingredients/` },
        { ...this.recipe, ingredients: updatedIngredients }
      );
      cy.spy(axios, 'request')
        .withArgs({
          method: 'patch',
          url: `${apiUrl}/recipes/${this.recipe.id}/ingredients/`,
          data: {
            ingredients: [1, 2, 3, 4, 5, 6, 7, 8, 9]
          },
          headers: {
            authorization: `Bearer ${token}`
          }
        })
        .as('updateRecipeIngredients');
    });

    cy.getTestSelector('recipe-ingredients-pagination-pagination')
      .find('button[aria-label="Next page"]')
      .click()
      .wait(1000)

      .getTestSelector('recipe-ingredients-dialog-button')
      .click();

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    cy.getTestSelector('recipe-ingredients-dialog-select-card-10')
      .click()
      .getTestSelector('recipe-ingredients-dialog-select-add-button')
      .click();

    for (const id of [1, 2, 3, 4, 5]) {
      cy.getTestSelector(`recipe-ingredients-pagination-${id}`).should('be.exist');
    }
  });
});
