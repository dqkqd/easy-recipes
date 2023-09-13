import IngredientViewBanner from '@/components/IngredientViewBanner.vue';
import { h } from 'vue';

beforeEach(() => {
  cy.mount(() => h(IngredientViewBanner));
});

it('Render', () => {
  cy.get('[data-test=ingredient-view-banner] img')
    .should('have.attr', 'src', '/ingredient-cover.jpg')

    .get('[data-test=ingredient-view-banner] [data-test=base-view-banner-title]')
    .should('contain.text', 'Ready to explore more ingredients?')

    .get('[data-test=ingredient-view-banner] [data-test=base-view-banner-button]')
    .should('be.visible');
});

it('New ingredient button', () => {
  cy.get('[data-test=ingredient-view-banner-card-ingredient-create]')
    .should('not.exist')
    .get('[data-test=ingredient-view-banner] [data-test=base-view-banner-button]')
    .click()
    .get('[data-test=ingredient-view-banner-card-ingredient-create]')
    .should('be.visible');
});
