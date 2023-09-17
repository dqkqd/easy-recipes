import MainAppBar from '@/components/MainAppBar.vue';
import router from '@/router';
import { h } from 'vue';

it('Render properly', () => {
  cy.mount(() => h(MainAppBar))

    .getTestSelector('main-app-bar-home-button')
    .should('have.text', 'Easy Recipes')
    .getTestSelector('main-app-bar-recipes-button')
    .should('have.text', 'Recipes')
    .getTestSelector('main-app-bar-ingredients-button')
    .should('have.text', 'Ingredients');
});

[
  { selector: 'main-app-bar-home-button', page: 'home' },
  { selector: 'main-app-bar-recipes-button', page: 'RecipeView' },
  { selector: 'main-app-bar-ingredients-button', page: 'IngredientView' }
].forEach((data: { selector: string; page: string }) => {
  it(`Move to ${data.page} when clicking ${data.page}'s button`, () => {
    cy.spy(router, 'push').withArgs({ name: data.page }).as('redirect');

    cy.mount(() => h(MainAppBar))
      .getTestSelector(data.selector)
      .click()

      .get('@redirect')
      .should('be.called');
  });
});
