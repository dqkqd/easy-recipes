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
  cy.getTestSelector('ingredient-details-name')
    .should('have.text', this.ingredient.name)

    .getTestSelector('ingredient-details-image')
    .find('img')
    .should('have.attr', 'src', this.ingredient.image_uri)

    .getTestSelector('ingredient-details-description')
    .should('have.text', this.ingredient.description)

    .getTestSelector('ingredient-details-like-button')
    .should('be.visible');
});
