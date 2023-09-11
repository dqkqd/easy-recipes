import RecipeDetails from '@/components/RecipeDetails.vue';
import { apiUrl } from '@/env';
import { h } from 'vue';

beforeEach(() => {
  cy.fixture('recipes/details/1.json')
    .as('recipe')
    .then((recipe) => {
      cy.mount(() => h(RecipeDetails, { recipe: recipe }));
    });
});

it('Render properly', function () {
  cy.get('[data-test=recipe-details-name]')
    .should('have.text', this.recipe.name)

    .get('[data-test=recipe-details-image] img')
    .should('have.attr', 'src', this.recipe.image_uri)

    .get('[data-test=recipe-details-description]')
    .should('have.text', this.recipe.description)

    .get('[data-test=recipe-details-like]')
    .should('be.visible')

    // TODO(khanhdq): authorization
    .get('[data-test=recipe-details-update-button]')
    .should('be.visible')

    .get('[data-test=recipe-details-delete-button]')
    .should('be.visible');
});

describe('Update recipe', () => {
  beforeEach(() => {
    cy.get('[data-test=recipe-details-update-dialog]')
      .should('not.exist')
      .get('[data-test=recipe-details-update-button]')
      .click()
      .get('[data-test=recipe-details-update-dialog]')
      .should('be.visible');
  });
  it('Updating recipe close update dialog and show success dialog', function () {
    cy.fixture('recipes/details/2.json').then((secondRecipe) => {
      const recipe = { ...this.recipe };
      recipe.name = secondRecipe.name;
      recipe.image_uri = secondRecipe.image_uri;
      recipe.description = secondRecipe.description;

      cy.intercept({ method: 'patch', url: `${apiUrl}/recipes/${recipe.id}` }, { ...recipe });

      cy.get('[data-test=form-recipe-name] input')
        .clear()
        .type(recipe.name)
        .get('[data-test=form-recipe-description] textarea')
        .clear()
        .type(recipe.description)
        .get('[data-test=form-image-input-url] input')
        .clear()
        .type(recipe.image_uri)

        .get('[data-test=form-recipe-submit-button]')
        .click()

        .get('[data-test=recipe-details-update-dialog')
        .should('not.exist')

        .get('[data-test=card-recipe-update-updated-dialog]')
        .should('be.visible')

        .get('[data-test=card-recipe-update-updated-dialog]')
        .should('not.exist');
    });
  });
});
it('Reload recipe after updating');
it('Show number of people liked if there are any');
it('Do not show number of people liked if there are none');
it('Clicking edit button open edit form');
it('Click cancel on update dialog should close dialog');
it('Click cancel on delete dialog should close dialog');
