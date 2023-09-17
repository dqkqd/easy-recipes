import FormIngredient from '@/components/FormIngredient.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render passed ingredient', () => {
    cy.fixture('ingredients/details/1.json').then((ingredient) => {
      cy.mount(() => h(FormIngredient, { ingredient: ingredient }))
        .getTestSelector('form-ingredient')
        .findTestSelector('base-form-name')
        .find('input')
        .should('have.value', ingredient.name)

        .getTestSelector('form-ingredient')
        .findTestSelector('base-form-description')
        .find('textarea')
        .should('have.value', ingredient.description)

        .getTestSelector('form-image-input-image')
        .find('img')
        .should('have.attr', 'src', ingredient.image_uri);
    });
  });
});

describe('Submit', () => {
  it('Success', () => {
    cy.fixture('recipes/create/1.json')
      .as('validRecipe')
      .then((recipe) => {
        cy.mount(() =>
          h(FormIngredient, {
            onSubmit: cy.spy().as('onSubmit')
          })
        )
          .getTestSelector('form-ingredient')
          .findTestSelector('base-form-name')
          .type(recipe.name)
          .getTestSelector('form-ingredient')
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
        .getTestSelector('form-ingredient')
        .findTestSelector('base-form-name')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-ingredient')
        .findTestSelector('base-form-description')
        .find('textarea')
        .should('not.be.disabled')
        .getTestSelector('form-image-input-file')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-image-input-url')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-ingredient')
        .findTestSelector('base-form-submit-button')
        .should('not.be.disabled');
    });

    it('default', () => {
      cy.mount(() => h(FormIngredient));
    });

    it('Loading=false', () => {
      cy.mount(() => h(FormIngredient, { loading: false }));
    });
  });

  describe('Loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('be.visible')
        .getTestSelector('form-ingredient')
        .findTestSelector('base-form-name')
        .find('input')
        .should('be.disabled')
        .getTestSelector('form-ingredient')
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
      cy.getTestSelector('form-ingredient').findTestSelector('base-form-submit-button').click({
        timeout: 100
      });
    });

    it('Loading=true', () => {
      cy.mount(() => h(FormIngredient, { loading: true }));
    });
  });
});
