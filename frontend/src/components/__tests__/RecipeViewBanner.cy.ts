import RecipeViewBanner from '@/components/RecipeViewBanner.vue';
import { h } from 'vue';

describe('Render', () => {
  afterEach(() => {
    cy.getTestSelector('recipe-view-banner')
      .find('img')
      .should('have.attr', 'src', '/recipe-cover.jpg')

      .getTestSelector('recipe-view-banner')
      .findTestSelector('base-view-banner-title')
      .should('contain.text', 'Ready to explore more recipes?');
  });

  describe('Render without create permission', () => {
    afterEach(() => {
      cy.getTestSelector('recipe-view-banner')
        .findTestSelector('base-view-banner-button')
        .should('not.exist');
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
      .getTestSelector('recipe-view-banner')
      .findTestSelector('base-view-banner-button')
      .should('be.visible');
  });
});

it('New recipe button', () => {
  cy.signJWT(true, ['create:recipe']).then(() => {
    cy.mount(() => h(RecipeViewBanner))
      .getTestSelector('recipe-view-banner-card-recipe-create')
      .should('not.exist')
      .getTestSelector('recipe-view-banner')
      .findTestSelector('base-view-banner-button')
      .click()
      .getTestSelector('recipe-view-banner-card-recipe-create')
      .should('be.visible');
  });
});
