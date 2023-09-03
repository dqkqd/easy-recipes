import CardRecipeCreate from '@/components/cards/CardRecipeCreate.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import { RecipeCreateSchema } from '@/schema/recipe';
import axios from 'axios';

beforeEach(() => {
  cy.fixture('recipes/1.json').as('validRecipe');
});

it('Render properly', () => {
  cy.mount(CardRecipeCreate);

  cy.get('[data-test="card-recipe-create-title"]').should('have.text', 'Add new recipe');

  cy.get('[data-test="card-form-recipe-create-name"]')
    .find('label')
    .first()
    .should('have.text', 'Name *');

  cy.get('[data-test="card-form-recipe-create-image-uri"]')
    .find('label')
    .first()
    .should('have.text', 'Image URL *');

  cy.get('[data-test="card-form-recipe-create-description"]')
    .find('label')
    .first()
    .should('have.text', 'Description');

  cy.get('[data-test="card-form-recipe-create-submit-button"]').should('have.text', 'ADD');
});

it('Mock create valid recipe', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipe);
  cy.mount(CardRecipeCreate);
  cy.intercept({ method: 'POST', url: `${apiUrl}/recipes/` }, { id: 1 }).as('createRecipe');
  cy.spy(axios, 'request')
    .withArgs({
      method: 'post',
      url: `${apiUrl}/recipes/`,
      data: recipe,
      headers: {
        authorization: 'bearer create:recipe'
      }
    })
    .as('requestToBackEnd');
  cy.spy(router, 'push')
    .withArgs({ name: 'RecipeDetails', params: { id: 1 } })
    .as('redirectedToRecipeDetails');

  cy.get('[data-test="card-form-recipe-create-name"]').find('input').type(recipe.name);
  cy.get('[data-test="card-form-recipe-create-image-uri"]').find('input').type(recipe.image_uri!);
  cy.get('[data-test="card-form-recipe-create-description"]')
    .find('textarea')
    .type(recipe.description!);

  cy.get('[data-test="card-form-recipe-create-submit-button"]').click();
  cy.get('@requestToBackEnd').should('be.called');
  cy.wait('@createRecipe');
  cy.get('@redirectedToRecipeDetails').should('be.called');
});

it('Mock create recipe with empty name', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipe);
  cy.mount(CardRecipeCreate);
  cy.spy(axios, 'request').as('requestToBackEnd');

  cy.get('[data-test="card-form-recipe-create-image-uri"]').find('input').type(recipe.image_uri!);

  cy.get('[class=v-form]').should('not.contain.text', 'Name is required');
  cy.get('[data-test="card-form-recipe-create-submit-button"]').click();
  cy.get('@requestToBackEnd').should('not.be.called');
  cy.get('[class=v-form]').should('contain.text', 'Name is required');
});

it('Mock create recipe with empty url', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipe);
  cy.mount(CardRecipeCreate);
  cy.spy(axios, 'request').as('requestToBackEnd');

  cy.get('[data-test="card-form-recipe-create-name"]').find('input').type(recipe.name);

  cy.get('[class=v-form]').should('not.contain.text', 'Invalid URL');
  cy.get('[data-test="card-form-recipe-create-submit-button"]').click();
  cy.get('@requestToBackEnd').should('not.be.called');
  cy.get('[class=v-form]').should('contain.text', 'Invalid URL');
});

it('Mock create recipe with invalid url', function () {
  cy.mount(CardRecipeCreate);
  cy.spy(axios, 'request').as('requestToBackEnd');

  cy.get('[data-test="card-form-recipe-create-image-uri"]')
    .find('input')
    .type('this-is-invalid-uri');

  cy.get('[class=v-form]').should('contain.text', 'Invalid URL');
});

it('Create valid recipe with loading', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipe);
  cy.mount(CardRecipeCreate);
  cy.intercept({ method: 'POST', url: `${apiUrl}/recipes/` }, { id: 1 }).as('createRecipe');

  cy.get('[data-test="card-form-recipe-create-name"]').find('input').type(recipe.name);
  cy.get('[data-test="card-form-recipe-create-image-uri"]').find('input').type(recipe.image_uri!);
  cy.get('[data-test="card-form-recipe-create-description"]')
    .find('textarea')
    .type(recipe.description!);
  cy.get('[data-test="card-form-recipe-create-submit-button"]').click();

  // should be loading and everything is disabled
  cy.get('.v-progress-circular').should('exist');
  cy.get('[data-test="card-form-recipe-create-name"]')
    .find('input')
    .should('have.attr', 'disabled');
  cy.get('[data-test="card-form-recipe-create-image-uri"]')
    .find('input')
    .should('have.attr', 'disabled');
  cy.get('[data-test="card-form-recipe-create-description"]')
    .find('textarea')
    .should('have.attr', 'disabled');

  cy.wait('@createRecipe');

  // should not be loading
  cy.get('.v-progress-circular').should('not.exist');
  cy.get('[data-test="card-form-recipe-create-name"]')
    .find('input')
    .should('not.have.attr', 'disabled');
  cy.get('[data-test="card-form-recipe-create-image-uri"]')
    .find('input')
    .should('not.have.attr', 'disabled');
  cy.get('[data-test="card-form-recipe-create-description"]')
    .find('textarea')
    .should('not.have.attr', 'disabled');
});
