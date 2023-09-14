import CardIngredient from '@/components/CardIngredient.vue';
import { IngredientSchema } from '@/schema/ingredient';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('ingredients/details/1.json').as('validIngredient');
});

it('Render properly', function () {
  const ingredient = IngredientSchema.parse(this.validIngredient);
  cy.mount(() => h(CardIngredient, { ingredient: ingredient }))

    .get('[data-test="card-ingredient-name"]')
    .should('have.text', ingredient.name)
    .get('[data-test="card-ingredient-image"] img')
    .should('have.attr', 'src', ingredient.image_uri);
});
