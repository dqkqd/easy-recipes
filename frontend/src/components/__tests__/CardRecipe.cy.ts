import CardRecipe from '@/components/CardRecipe.vue';
import router from '@/router';
import { RecipeSchema } from '@/schema/recipe';
import { h } from 'vue';

beforeEach(() => {
  cy.wrap({
    id: 1,
    name: 'My first recipe',
    description: 'My first description',
    image_uri: 'https://picsum.photos/200',
    ingredients: [],
    likes: 2
  }).as('validRecipe');
});

describe('Render', () => {
  it('Render name less than 20 characters', function () {
    const recipe = RecipeSchema.parse(this.validRecipe);
    cy.mount(() => h(CardRecipe, { recipe: recipe }))
      .getTestSelector('card-recipe-name')
      .should('have.text', recipe.name)
      .getTestSelector('card-recipe-image')
      .find('img')
      .should('have.attr', 'src', recipe.image_uri);
  });

  it('Render name more than 20 characters', function () {
    const recipe = RecipeSchema.parse({
      id: 1,
      name: 'This is my first recipe',
      description: 'My first description',
      image_uri: 'https://picsum.photos/200',
      ingredients: [],
      likes: 3
    });

    cy.mount(() => h(CardRecipe, { recipe: recipe }))
      .getTestSelector('card-recipe-name')
      .should('have.text', 'This is my first re…')
      .getTestSelector('card-recipe-image')
      .find('img')
      .should('have.attr', 'src', recipe.image_uri);
  });
});

it('Mock move to recipe info', function () {
  const recipe = RecipeSchema.parse(this.validRecipe);
  cy.spy(router, 'push')
    .withArgs({ name: 'RecipeInfo', params: { id: 1 } })
    .as('redirectedToRecipeInfo');

  cy.mount(() => h(CardRecipe, { recipe: recipe }))
    .getTestSelector('card-to-recipe-details')
    .click()

    .get('@redirectedToRecipeInfo')
    .should('be.called');
});
