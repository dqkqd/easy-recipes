import IngredientDetails from '@/components/IngredientDetails.vue';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('ingredients/details/1.json')
    .as('ingredient')
    .then((ingredient) => {
      cy.mount(() => h(IngredientDetails, { ingredient: ingredient }));
    });
});

it('Render properly', function () {
  cy.get('[data-test=ingredient-details-name]')
    .should('have.text', this.ingredient.name)

    .get('[data-test=ingredient-details-image] img')
    .should('have.attr', 'src', this.ingredient.image_uri)

    .get('[data-test=ingredient-details-description]')
    .should('have.text', this.ingredient.description)

    .get('[data-test=ingredient-details-like]')
    .should('be.visible');
});

it('Show number of people liked if there are any');
it('Do not show number of people liked if there are none');
