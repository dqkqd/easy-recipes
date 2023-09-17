import FormRecipe from '@/components/FormRecipe.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render passed recipe', () => {
    cy.fixture('recipes/details/1.json').then((recipe) => {
      cy.mount(() => h(FormRecipe, { recipe: recipe }))
        .getTestSelector('form-recipe')
        .findTestSelector('base-form-name')
        .find('input')
        .should('have.value', recipe.name)

        .getTestSelector('form-recipe')
        .findTestSelector('base-form-description')
        .find('textarea')
        .should('have.value', recipe.description)

        .getTestSelector('form-image-input-image')
        .find('img')
        .should('have.attr', 'src', recipe.image_uri);
    });
  });
});

describe('Submit', () => {
  it('Success', () => {
    cy.fixture('recipes/create/1.json')
      .as('validRecipe')
      .then((recipe) => {
        cy.mount(() =>
          h(FormRecipe, {
            onSubmit: cy.spy().as('onSubmit')
          })
        )
          .getTestSelector('form-recipe')
          .findTestSelector('base-form-name')
          .type(recipe.name)
          .getTestSelector('form-recipe')
          .findTestSelector('base-form-description')
          .type(recipe.description);
      });
  });
});

describe('Loading', () => {
  describe('No loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('not.exist')
        .getTestSelector('form-recipe')
        .findTestSelector('base-form-name')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-recipe')
        .findTestSelector('base-form-description')
        .find('textarea')
        .should('not.be.disabled')
        .getTestSelector('form-image-input-file')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-image-input-url')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-recipe')
        .findTestSelector('base-form-submit-button')
        .should('not.be.disabled');
    });

    it('default', () => {
      cy.mount(() => h(FormRecipe));
    });

    it('Loading=false', () => {
      cy.mount(() => h(FormRecipe, { loading: false }));
    });
  });

  describe('Loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('be.visible')
        .getTestSelector('form-recipe')
        .findTestSelector('base-form-name')
        .find('input')
        .should('be.disabled')
        .getTestSelector('form-recipe')
        .findTestSelector('base-form-description')
        .find('textarea')
        .should('be.disabled')
        .getTestSelector('form-image-input-file')
        .find('input')
        .should('be.disabled')
        .getTestSelector('form-image-input-url')
        .find('input')
        .should('be.disabled');

      cy.once('fail', (err) => {
        expect(err.message).to.include('`cy.click()` failed because this element');
        expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
      });
      cy.getTestSelector('form-recipe')
        .findTestSelector('base-form-submit-button')
        .click({ timeout: 100 });
    });

    it('Loading=true', () => {
      cy.mount(() => h(FormRecipe, { loading: true }));
    });
  });
});
