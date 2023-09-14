import CardIngredient from '@/components/CardIngredient.vue';
import { IngredientSchema } from '@/schema/ingredient';
import { h } from 'vue';

describe('Render', () => {
  it('Render name less than 10 characters', function () {
    const ingredient = IngredientSchema.parse({
      id: 1,
      name: 'Ingredient',
      description: 'My first ingredient description',
      image_uri: 'https://picsum.photos/200',
      recipes: []
    });

    cy.mount(() => h(CardIngredient, { ingredient: ingredient }))
      .get('[data-test="card-ingredient-name"]')
      .should('have.text', ingredient.name)
      .get('[data-test="card-ingredient-image"] img')
      .should('have.attr', 'src', ingredient.image_uri);
  });

  it('Render name more than 10 characters', function () {
    const ingredient = IngredientSchema.parse({
      id: 1,
      name: 'My first ingredient',
      description: 'My first ingredient description',
      image_uri: 'https://picsum.photos/200',
      recipes: []
    });

    cy.mount(() => h(CardIngredient, { ingredient: ingredient }))
      .get('[data-test="card-ingredient-name"]')
      .should('have.text', 'My first …')
      .get('[data-test="card-ingredient-image"] img')
      .should('have.attr', 'src', ingredient.image_uri);
  });
});
