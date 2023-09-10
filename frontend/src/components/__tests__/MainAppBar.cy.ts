import MainAppBar from '@/components/MainAppBar.vue';
import router from '@/router';
import { h } from 'vue';

it('Render properly', () => {
  cy.mount(() => h(MainAppBar))

    .get('[data-test="main-app-bar-home-button"]')
    .should('have.text', 'Easy Recipes')
    .get('[data-test="main-app-bar-recipes-button"]')
    .should('have.text', 'Recipes')
    .get('[data-test="main-app-bar-ingredients-button"]')
    .should('have.text', 'Ingredients');
});

[
  { selector: '[data-test=main-app-bar-home-button]', page: 'home' },
  { selector: '[data-test=main-app-bar-recipes-button]', page: 'RecipeView' },
  { selector: '[data-test=main-app-bar-ingredients-button]', page: 'IngredientView' }
].forEach((data: { selector: string; page: string }) => {
  it(`Move to ${data.page} when clicking ${data.page}'s button`, () => {
    cy.spy(router, 'push').withArgs({ name: data.page }).as('redirect');

    cy.mount(() => h(MainAppBar))
      .get(data.selector)
      .click()

      .get('@redirect')
      .should('be.called');
  });
});
