import RecipeIngredientsDialogSelect from '@/components/RecipeIngredientsDialogSelect.vue';
import { apiUrl } from '@/env';
import { RECIPE_INGREDIENT_PER_PAGE } from '@/utils';
import axios from 'axios';
import { h } from 'vue';

beforeEach(() => {
  const query = {
    per_page: `${RECIPE_INGREDIENT_PER_PAGE}`
  };
  cy.wrap(query).as('query');

  const params = new URLSearchParams(query);
  const request = cy.spy(axios, 'request').as('request');

  request
    .withArgs({
      method: 'get',
      url: `${apiUrl}/ingredients/`,
      params
    })
    .as('pageOneRequest');

  params.append('page', '2');
  request
    .withArgs({
      method: 'get',
      url: `${apiUrl}/ingredients/`,
      params
    })
    .as('pageTwoRequest');
});

describe('Render', () => {
  describe('Success', () => {
    beforeEach(function () {
      cy.fixture('ingredients/pages/1.json').then((ingredients) => {
        cy.intercept(
          { method: 'get', url: `${apiUrl}/ingredients/*`, query: this.query },
          ingredients
        );
      });
    });

    afterEach(() => {
      cy.getTestSelector('recipe-ingredients-dialog-select-title')
        .should('have.text', 'Add more ingredients')

        .getTestSelector('recipe-ingredients-dialog-select-add-button')
        .should('have.text', 'Select')

        .getTestSelector('recipe-ingredients-dialog-select-error')
        .should('not.exist')

        .getTestSelector('recipe-ingredients-dialog-select-pagination')
        .should('be.visible')

        .get('@pageOneRequest')
        .should('have.been.calledOnce');

      for (let id = 1; id <= 5; ++id) {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`).should('be.visible');
      }
    });

    it('Render with selected ids', function () {
      const selectedIds = [1, 2, 5];
      cy.mount(() =>
        h(RecipeIngredientsDialogSelect, {
          selectedIds
        })
      );

      for (let id = 1; id <= 5; ++id) {
        if (selectedIds.includes(id)) {
          cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
            .findTestSelector('recipe-ingredients-dialog-select-card')
            .should('have.class', 'selected');
        } else {
          cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
            .findTestSelector('recipe-ingredients-dialog-select-card')
            .should('not.have.class', 'selected');
        }
      }
    });

    it('Render without selected ids', () => {
      cy.mount(() =>
        h(RecipeIngredientsDialogSelect, {
          selectedIds: []
        })
      );
      for (let id = 1; id <= 5; ++id) {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('not.have.class', 'selected');
      }
    });
  });

  describe('Failed', () => {
    it('Render with error', function () {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/ingredients/*`, query: this.query },
        { forceNetworkError: true }
      );

      cy.mount(() =>
        h(RecipeIngredientsDialogSelect, {
          selectedIds: []
        })
      )
        .getTestSelector('recipe-ingredients-dialog-select-error')
        .should('be.visible');
    });
  });
});

describe('Select ids', () => {
  beforeEach(function () {
    cy.fixture('ingredients/pages/1.json').then((ingredients) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/ingredients/*`, query: this.query },
        ingredients
      );
    });
  });
  it('Toggle select ids', () => {
    cy.mount(() =>
      h(RecipeIngredientsDialogSelect, {
        selectedIds: [1, 2, 3]
      })
    );

    cy.getTestSelector(`recipe-ingredients-dialog-select-card-1`)
      .findTestSelector('recipe-ingredients-dialog-select-card')
      .should('have.class', 'selected')
      .click()
      .should('not.have.class', 'selected')
      .click()
      .should('have.class', 'selected');

    cy.getTestSelector(`recipe-ingredients-dialog-select-card-4`)
      .findTestSelector('recipe-ingredients-dialog-select-card')
      .should('not.have.class', 'selected')
      .click()
      .should('have.class', 'selected');
  });
});

describe('Pagination', () => {
  beforeEach(function () {
    cy.fixture('ingredients/pages/1.json').then((ingredients) => {
      cy.intercept(
        { method: 'get', url: `${apiUrl}/ingredients/*`, query: this.query },
        ingredients
      );
    });

    const query = {
      page: '2',
      per_page: `${RECIPE_INGREDIENT_PER_PAGE}`
    };

    cy.fixture('ingredients/pages/2.json').then((ingredients) => {
      cy.intercept({ method: 'get', url: `${apiUrl}/ingredients/*`, query }, ingredients);
    });
  });

  it('Move to page 2', function () {
    cy.mount(() =>
      h(RecipeIngredientsDialogSelect, {
        selectedIds: []
      })
    )
      .getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    cy.get('@pageTwoRequest').should('have.been.called');

    Cypress.on('uncaught:exception', () => {
      return false;
    });
  });

  it('Move to page 2 should show selected ingredients', function () {
    const selectedIds = [6, 7];
    cy.mount(() =>
      h(RecipeIngredientsDialogSelect, {
        selectedIds
      })
    );

    // page 1
    for (let id = 1; id <= 5; ++id) {
      cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
        .findTestSelector('recipe-ingredients-dialog-select-card')
        .should('not.have.class', 'selected');
    }

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    // page 2
    for (let id = 6; id <= 10; ++id) {
      if (selectedIds.includes(id)) {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('have.class', 'selected');
      } else {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('not.have.class', 'selected');
      }
    }
  });

  it('Move to page 2 then move back should keep selected ids', function () {
    cy.mount(() =>
      h(RecipeIngredientsDialogSelect, {
        selectedIds: [1, 2]
      })
    );

    cy.getTestSelector(`recipe-ingredients-dialog-select-card-1`).click();
    cy.getTestSelector(`recipe-ingredients-dialog-select-card-3`).click();

    // selectIds is now [2,3]
    const newSelectedIds = [2, 3];

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      })
      .getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '1') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    for (let id = 1; id <= 5; ++id) {
      if (newSelectedIds.includes(id)) {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('have.class', 'selected');
      } else {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('not.have.class', 'selected');
      }
    }
  });

  it('Move to page 2 the second times should keep selected ids', function () {
    cy.mount(() =>
      h(RecipeIngredientsDialogSelect, {
        selectedIds: [6, 7]
      })
    );

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    cy.getTestSelector(`recipe-ingredients-dialog-select-card-6`).click();
    cy.getTestSelector(`recipe-ingredients-dialog-select-card-8`).click();

    // selectIds is now [7,8]
    const newSelectedIds = [7, 8];

    cy.getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '1') {
          cy.wrap($elem).wait(1000).click();
        }
      })
      .getTestSelector('recipe-ingredients-dialog-select-pagination-pagination')
      .find('li button span')
      .each(($elem) => {
        if ($elem.text() === '2') {
          cy.wrap($elem).wait(1000).click();
        }
      });

    for (let id = 6; id <= 10; ++id) {
      if (newSelectedIds.includes(id)) {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('have.class', 'selected');
      } else {
        cy.getTestSelector(`recipe-ingredients-dialog-select-card-${id}`)
          .findTestSelector('recipe-ingredients-dialog-select-card')
          .should('not.have.class', 'selected');
      }
    }
  });
});
