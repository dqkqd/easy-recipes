import CardRecipe from '@/components/cards/CardRecipe.vue';
import router from '@/router';
import { RecipeSchema } from '@/schema/recipe';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json').as('validRecipe');
});

it('Render properly', function () {
  const recipe = RecipeSchema.parse(this.validRecipe);
  cy.mount(() => h(CardRecipe, { recipe: recipe }))

    .get('[data-test="card-recipe-name"]')
    .should('have.text', recipe.name)
    .get('[data-test="card-recipe-image"] img')
    .should('have.attr', 'src', recipe.image_uri);
});

it('Mock move to recipe info', function () {
  const recipe = RecipeSchema.parse(this.validRecipe);
  cy.spy(router, 'push')
    .withArgs({ name: 'RecipeInfo', params: { id: 1 } })
    .as('redirectedToRecipeInfo');

  cy.mount(() => h(CardRecipe, { recipe: recipe }))
    .get('[data-test="card-to-recipe-details"]')
    .click()

    .get('@redirectedToRecipeInfo')
    .should('be.called');
});
