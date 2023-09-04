import CardRecipe from '@/components/cards/CardRecipe.vue';
import router from '@/router';
import { RecipeSchema } from '@/schema/recipe';

beforeEach(() => {
  cy.fixture('recipes/details/1.json').as('validRecipeDetails');
});

it('Render properly', function () {
  const recipe = RecipeSchema.parse(this.validRecipeDetails);
  cy.mount(CardRecipe, { props: { recipe: recipe } })

    .get('[data-test="card-recipe-name"]')
    .should('have.text', recipe.name)
    .get('[data-test="card-recipe-image"] img')
    .should('have.attr', 'src', recipe.image_uri);
});

it('Mock move to recipe details', function () {
  const recipe = RecipeSchema.parse(this.validRecipeDetails);
  cy.spy(router, 'push')
    .withArgs({ name: 'RecipeDetails', params: { id: 1 } })
    .as('redirectedToRecipeDetails');

  cy.mount(CardRecipe, { props: { recipe: recipe } })
    .get('[data-test="card-to-recipe-details"]')
    .click()

    .get('@redirectedToRecipeDetails')
    .should('be.called');
});
