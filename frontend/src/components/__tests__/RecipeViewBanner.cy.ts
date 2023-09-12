import RecipeViewBanner from '@/components/RecipeViewBanner.vue';
import { h } from 'vue';

beforeEach(() => {
  cy.mount(() => h(RecipeViewBanner));
});

it('Render', () => {
  cy.get('[data-test=recipe-view-banner-cover-image] img')
    .should('have.attr', 'src', '/recipe-cover.jpg')

    .get('[data-test=recipe-view-banner-title]')
    .should('contain.text', 'Ready to explore more recipes?')

    .get('[data-test=recipe-view-banner-new-recipe-button]')
    .should('be.visible');
});

it('New recipe button', () => {
  cy.get('[data-test=recipe-view-banner-card-recipe-create]')
    .should('not.exist')
    .get('[data-test=recipe-view-banner-new-recipe-button]')
    .click()
    .get('[data-test=recipe-view-banner-card-recipe-create]')
    .should('be.visible')

    .get('[data-test=form-recipe-cancel-button]')
    .click()
    .get('[data-test=recipe-view-banner-card-recipe-create]')
    .should('not.exist');
});
