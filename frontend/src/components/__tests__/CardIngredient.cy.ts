import CardIngredient from '@/components/CardIngredient.vue';
import router from '@/router';
import { IngredientSchema } from '@/schema/ingredient';
import { h } from 'vue';

describe('Render', () => {
  it('Render name less than 10 characters', function () {
    const ingredient = IngredientSchema.parse({
      id: 1,
      name: 'Ingredient',
      description: 'My first ingredient description',
      image_uri: 'https://picsum.photos/200',
      recipes: [],
      likes: 10
    });

    cy.mount(() => h(CardIngredient, { ingredient: ingredient }))
      .getTestSelector('card-ingredient-name')
      .should('have.text', ingredient.name)
      .getTestSelector('card-ingredient-image')
      .find('img')
      .should('have.attr', 'src', ingredient.image_uri);
  });

  it('Render name more than 10 characters', function () {
    const ingredient = IngredientSchema.parse({
      id: 1,
      name: 'My first ingredient',
      description: 'My first ingredient description',
      image_uri: 'https://picsum.photos/200',
      recipes: [],
      likes: 10
    });

    cy.mount(() => h(CardIngredient, { ingredient: ingredient }))
      .getTestSelector('card-ingredient-name')
      .should('have.text', 'My first …')
      .getTestSelector('card-ingredient-image')
      .find('img')
      .should('have.attr', 'src', ingredient.image_uri);
  });
});

describe('Ingredient details dialog', () => {
  it('Show ingredient details after clicking', () => {
    const ingredient = IngredientSchema.parse({
      id: 1,
      name: 'Ingredient',
      description: 'My first ingredient description',
      image_uri: 'https://picsum.photos/200',
      recipes: [],
      likes: 10
    });

    cy.spy(router, 'push')
      .withArgs({ name: 'IngredientInfo', params: { id: 1 } })
      .as('redirectedToIngredientInfo');

    cy.mount(() => h(CardIngredient, { ingredient: ingredient }))

      .getTestSelector('card-to-ingredient-details')
      .click()

      .get('@redirectedToIngredientInfo')
      .should('be.called');
  });
});
