import IngredientViewBanner from '@/components/IngredientViewBanner.vue';
import { h } from 'vue';

describe('Render', () => {
  afterEach(() => {
    cy.get('[data-test=ingredient-view-banner] img')
      .should('have.attr', 'src', '/ingredient-cover.jpg')

      .get('[data-test=ingredient-view-banner] [data-test=base-view-banner-title]')
      .should('contain.text', 'Ready to explore more ingredients?');
  });

  describe('Render without create permission', () => {
    afterEach(() => {
      cy.get('[data-test=ingredient-view-banner] [data-test=base-view-banner-button]').should(
        'not.exist'
      );
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
      .get('[data-test=ingredient-view-banner] [data-test=base-view-banner-button]')
      .should('be.visible');
  });
});

it('New ingredient button', () => {
  cy.signJWT(true, ['create:ingredient']).then(() => {
    cy.mount(() => h(IngredientViewBanner))
      .get('[data-test=ingredient-view-banner-card-ingredient-create]')
      .should('not.exist')
      .get('[data-test=ingredient-view-banner] [data-test=base-view-banner-button]')
      .click()
      .get('[data-test=ingredient-view-banner-card-ingredient-create]')
      .should('be.visible');
  });
});
