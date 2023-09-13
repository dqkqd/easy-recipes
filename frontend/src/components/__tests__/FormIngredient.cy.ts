import FormIngredient from '@/components/FormIngredient.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render passed ingredient', () => {
    cy.fixture('ingredients/details/1.json').then((ingredient) => {
      cy.mount(() => h(FormIngredient, { ingredient: ingredient }))
        .get('[data-test=form-ingredient] [data-test=base-form-name] input')
        .should('have.value', ingredient.name)

        .get('[data-test=form-ingredient] [data-test=base-form-description] textarea')
        .should('have.value', ingredient.description)

        .get('[data-test=form-image-input-image] img')
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
          .get('[data-test=form-ingredient] [data-test=base-form-name]')
          .type(recipe.name)
          .get('[data-test=form-ingredient] [data-test=base-form-description]')
          .type(recipe.description);
      });
  });
});

describe('Loading', () => {
  describe('No loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('not.exist')
        .get('[data-test=form-ingredient] [data-test=base-form-name] input')
        .should('not.be.disabled')
        .get('[data-test=form-ingredient] [data-test=base-form-description] textarea')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('not.be.disabled')
        .get('[data-test=form-ingredient] [data-test=base-form-submit-button]')
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
        .get('[data-test=form-ingredient] [data-test=base-form-name] input')
        .should('be.disabled')
        .get('[data-test=form-ingredient] [data-test=base-form-description] textarea')
        .should('be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('be.disabled');

      cy.once('fail', (err) => {
        expect(err.message).to.include('`cy.click()` failed because this element');
        expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
      });
      cy.get('[data-test=form-ingredient] [data-test=base-form-submit-button]').click({
        timeout: 100
      });
    });

    it('Loading=true', () => {
      cy.mount(() => h(FormIngredient, { loading: true }));
    });
  });
});
