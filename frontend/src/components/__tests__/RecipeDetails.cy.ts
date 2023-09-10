import RecipeDetails from '@/components/RecipeDetails.vue';
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
    .get('[data-test=recipe-details-update-button]')
    .should('be.visible')

    .get('[data-test=recipe-details-delete-button]')
    .should('be.visible');
});

it('Reload recipe after updating');
it('Show number of people liked if there are any');
it('Do not show number of people liked if there are none');
it('Clicking edit button open edit form');
it('Click cancel on update dialog should close dialog');
it('Click cancel on delete dialog should close dialog');
