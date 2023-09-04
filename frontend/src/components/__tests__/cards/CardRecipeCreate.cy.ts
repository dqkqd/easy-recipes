import CardRecipeCreate from '@/components/cards/CardRecipeCreate.vue';
import { apiUrl } from '@/env';
import router from '@/router';
import { RecipeCreateSchema } from '@/schema/recipe';
import axios from 'axios';

beforeEach(() => {
  cy.fixture('recipes/create/1.json').as('validRecipeCreate');
});

it('Render properly', () => {
  cy.mount(CardRecipeCreate)

    .get('[data-test="card-recipe-create-title"]')
    .should('have.text', 'Add new recipe')
    .get('[data-test="card-form-recipe-create-name"] label')
    .first()
    .should('have.text', 'Name *')
    .get('[data-test="card-form-recipe-create-image-uri"] label')
    .first()
    .should('have.text', 'Image URL *')
    .get('[data-test="card-form-recipe-create-description"] label')
    .first()
    .should('have.text', 'Description')
    .get('[data-test="card-form-recipe-create-submit-button"]')
    .should('have.text', 'ADD');
});

it('Mock create valid recipe', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipeCreate);

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

  cy.mount(CardRecipeCreate)
    .get('[data-test="card-form-recipe-create-name"] input')
    .type(recipe.name)
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .type(recipe.image_uri!)
    .get('[data-test="card-form-recipe-create-description"] textarea')
    .type(recipe.description!)
    .get('[data-test="card-form-recipe-create-submit-button"]')
    .click()

    .get('@requestToBackEnd')
    .should('be.called')

    .wait('@createRecipe')

    .get('@redirectedToRecipeDetails')
    .should('be.called');
});

it('Mock create recipe with empty name', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipeCreate);
  cy.spy(axios, 'request').as('requestToBackEnd');

  cy.mount(CardRecipeCreate)
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .type(recipe.image_uri!)

    .get('[class=v-form]')
    .should('not.contain.text', 'Name is required')

    .get('[data-test="card-form-recipe-create-submit-button"]')
    .click()

    .get('@requestToBackEnd')
    .should('not.be.called')
    .get('[class=v-form]')
    .should('contain.text', 'Name is required');
});

it('Mock create recipe with empty url', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipeCreate);
  cy.spy(axios, 'request').as('requestToBackEnd');

  cy.mount(CardRecipeCreate)
    .get('[data-test="card-form-recipe-create-name"] input')
    .type(recipe.name)

    .get('[class=v-form]')
    .should('not.contain.text', 'Invalid URL')

    .get('[data-test="card-form-recipe-create-submit-button"]')
    .click()

    .get('@requestToBackEnd')
    .should('not.be.called')
    .get('[class=v-form]')
    .should('contain.text', 'Invalid URL');
});

it('Mock create recipe with invalid url', function () {
  cy.spy(axios, 'request').as('requestToBackEnd');

  cy.mount(CardRecipeCreate)
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .type('this-is-invalid-uri')

    .get('[class=v-form]')
    .should('contain.text', 'Invalid URL');
});

it('Create valid recipe with loading', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipeCreate);
  cy.intercept({ method: 'POST', url: `${apiUrl}/recipes/` }, { id: 1 }).as('createRecipe');

  cy.mount(CardRecipeCreate)
    .get('[data-test="card-form-recipe-create-name"] input')
    .type(recipe.name)
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .type(recipe.image_uri!)
    .get('[data-test="card-form-recipe-create-description"] textarea')
    .type(recipe.description!)
    .get('[data-test="card-form-recipe-create-submit-button"]')
    .click()

    .get('.v-progress-circular')
    .should('exist')
    .get('[data-test="card-form-recipe-create-name"] input')
    .should('have.attr', 'disabled')
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .should('have.attr', 'disabled')
    .get('[data-test="card-form-recipe-create-description"] textarea')
    .should('have.attr', 'disabled')

    .wait('@createRecipe')

    .get('.v-progress-circular').should('not.exist')
    .get('[data-test="card-form-recipe-create-name"] input')
    .should('not.have.attr', 'disabled')
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .should('not.have.attr', 'disabled')
    .get('[data-test="card-form-recipe-create-description"] textarea')
    .should('not.have.attr', 'disabled');
});

it('Mock create recipe with network error', function () {
  const recipe = RecipeCreateSchema.parse(this.validRecipeCreate);
  cy.intercept({ method: 'POST', url: `${apiUrl}/recipes/`, times: 1 }, { forceNetworkError: true }).as('createRecipe');

  cy.spy(router, 'push').as('redirectedToRecipeDetails');

  cy.mount(CardRecipeCreate)
    .get('[data-test="card-form-recipe-create-name"] input')
    .type(recipe.name)
    .get('[data-test="card-form-recipe-create-image-uri"] input')
    .type('https://example.com/')
    .get('[data-test="card-form-recipe-create-description"] textarea')
    .type(recipe.description!)
    .get('[data-test="card-form-recipe-create-submit-button"]')
    .click()
    .wait('@createRecipe')

    .get('@redirectedToRecipeDetails')
    .should('not.be.called')
    .get('[data-test=card-form-recipe-create-error]')
    .should('exist');
});
