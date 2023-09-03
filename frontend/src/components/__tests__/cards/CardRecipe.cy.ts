import CardRecipe from '@/components/cards/CardRecipe.vue';
import router from '@/router';
import { RecipeSchema } from '@/schema/recipe';

beforeEach(() => {
  cy.fixture('recipes/details/1.json').as('validRecipeDetails');
});

it('Render properly', function () {
  const recipe = RecipeSchema.parse(this.validRecipeDetails);
  cy.mount(CardRecipe, { props: { recipe: recipe } });

  cy.get('[data-test="card-recipe-name"]').should('have.text', recipe.name);
  cy.get('[data-test="card-recipe-image"]')
    .find('img')
    .should('have.attr', 'src', recipe.image_uri);
});

it('Mock move to recipe details', function () {
  const recipe = RecipeSchema.parse(this.validRecipeDetails);
  cy.mount(CardRecipe, { props: { recipe: recipe } });

  cy.spy(router, 'push')
    .withArgs({ name: 'RecipeDetails', params: { id: 1 } })
    .as('redirectedToRecipeDetails');

  cy.get('[data-test="card-to-recipe-details"]').click();
  cy.get('@redirectedToRecipeDetails').should('be.called');
});
