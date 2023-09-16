import RecipeViewBanner from '@/components/RecipeViewBanner.vue';
import { h } from 'vue';

describe('Render', () => {
  afterEach(() => {
    cy.get('[data-test=recipe-view-banner] img')
      .should('have.attr', 'src', '/recipe-cover.jpg')

      .get('[data-test=recipe-view-banner] [data-test=base-view-banner-title]')
      .should('contain.text', 'Ready to explore more recipes?');
  });

  describe('Render without create permission', () => {
    afterEach(() => {
      cy.get('[data-test=recipe-view-banner] [data-test=base-view-banner-button]').should(
        'not.exist'
      );
    });

    it('Render without authentication', () => {
      cy.signJWT(false).then(() => {
        cy.mount(() => h(RecipeViewBanner));
      });
    });

    it('Render without create recipe permission', () => {
      cy.signJWT(true, ['create:ingredient']).then(() => {
        cy.mount(() => h(RecipeViewBanner));
      });
    });
  });
});

it('Render with create recipe permission', () => {
  cy.signJWT(true, ['create:recipe']).then(() => {
    cy.mount(() => h(RecipeViewBanner))
      .get('[data-test=recipe-view-banner] [data-test=base-view-banner-button]')
      .should('be.visible');
  });
});

it('New recipe button', () => {
  cy.signJWT(true, ['create:recipe']).then(() => {
    cy.mount(() => h(RecipeViewBanner))
      .get('[data-test=recipe-view-banner-card-recipe-create]')
      .should('not.exist')
      .get('[data-test=recipe-view-banner] [data-test=base-view-banner-button]')
      .click()
      .get('[data-test=recipe-view-banner-card-recipe-create]')
      .should('be.visible');
  });
});
