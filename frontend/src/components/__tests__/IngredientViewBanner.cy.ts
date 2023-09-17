import IngredientViewBanner from '@/components/IngredientViewBanner.vue';
import { h } from 'vue';

describe('Render', () => {
  afterEach(() => {
    cy.getTestSelector('ingredient-view-banner')
      .find('img')
      .should('have.attr', 'src', '/ingredient-cover.jpg')

      .getTestSelector('ingredient-view-banner')
      .findTestSelector('base-view-banner-title')
      .should('contain.text', 'Ready to explore more ingredients?');
  });

  describe('Render without create permission', () => {
    afterEach(() => {
      cy.getTestSelector('ingredient-view-banner')
        .findTestSelector('base-view-banner-button')
        .should('not.exist');
    });

    it('Render without authentication', () => {
      cy.signJWT(false).then(() => {
        cy.mount(() => h(IngredientViewBanner));
      });
    });

    it('Render without create ingredient permission', () => {
      cy.signJWT(true, ['create:recipe']).then(() => {
        cy.mount(() => h(IngredientViewBanner));
      });
    });
  });
});

it('Render with create ingredient permission', () => {
  cy.signJWT(true, ['create:ingredient']).then(() => {
    cy.mount(() => h(IngredientViewBanner))
      .getTestSelector('ingredient-view-banner')
      .findTestSelector('base-view-banner-button')
      .should('be.visible');
  });
});

it('New ingredient button', () => {
  cy.signJWT(true, ['create:ingredient']).then(() => {
    cy.mount(() => h(IngredientViewBanner))
      .getTestSelector('ingredient-view-banner-card-ingredient-create')
      .should('not.exist')
      .getTestSelector('ingredient-view-banner')
      .findTestSelector('base-view-banner-button')
      .click()
      .getTestSelector('ingredient-view-banner-card-ingredient-create')
      .should('be.visible');
  });
});
