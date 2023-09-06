import RecipeDetails from '@/components/recipes/RecipeDetails.vue';
import { RecipeSchema } from '@/schema/recipe';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json').as('validRecipeDetails');
});

it('Render properly', function () {
  const recipe = RecipeSchema.parse(this.validRecipeDetails);
  cy.mount(() => h(RecipeDetails, { recipe: recipe }))

    .get('[data-test=recipe-details-name]')
    .should('have.text', recipe.name)

    .get('[data-test=recipe-details-image] img')
    .should('have.attr', 'src', recipe.image_uri)

    .get('[data-test=recipe-details-description]')
    .should('have.text', recipe.description)

    .get('[data-test=recipe-details-like]')
    .should('be.visible')

    // TODO(khanhdq): authorization
    .get('[data-test=recipe-details-edit-button]')
    .should('be.visible')

    .get('[data-test=recipe-details-delete-button]')
    .should('be.visible');
});
