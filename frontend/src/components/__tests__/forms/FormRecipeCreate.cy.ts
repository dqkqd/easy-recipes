import FormRecipeCreate from '@/components/forms/FormRecipeCreate.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(FormRecipeCreate))

      .get('[data-test=form-recipe-create-name] label')
      .first()
      .should('have.text', 'Name *')

      .get('[data-test=form-recipe-create-description] label')
      .first()
      .should('have.text', 'Description')

      .get('[data-test=form-recipe-create-submit-button]')
      .should('have.text', 'Submit')

      .get('[data-test=form-recipe-create-cancel-button]')
      .should('have.text', 'Cancel');
  });
});

describe('Submit', () => {
  describe('Success', () => {
    beforeEach(() => {
      cy.fixture('recipes/create/1.json')
        .as('validRecipe')
        .then((recipe) => {
          cy.mount(() =>
            h(FormRecipeCreate, {
              onSubmit: cy.spy().as('onSubmit')
            })
          )
            .get('[data-test=form-recipe-create-name]')
            .type(recipe.name)
            .get('[data-test=form-recipe-create-description]')
            .type(recipe.description);
        });
    });

    it('No image selected', function () {
      cy.get('[data-test=form-recipe-create-submit-button]')
        .click()
        .get('@onSubmit')
        .should('have.been.calledWith', this.validRecipe.name, null, this.validRecipe.description);
    });

    it('Input image url', function () {
      cy.get('[data-test=form-image-input-url]')
        .type(this.validRecipe.image_uri)
        .get('[data-test=form-recipe-create-submit-button]')
        .click()
        .get('@onSubmit')
        .should(
          'have.been.calledWith',
          this.validRecipe.name,
          this.validRecipe.image_uri,
          this.validRecipe.description
        );
    });

    it('Input image file', function () {
      const file = 'cypress/fixtures/images/recipe.png';
      cy.get('[data-test=form-image-input-file] input')
        .selectFile(file)
        .get('[data-test=form-recipe-create-submit-button]')
        .click()
        .get('@onSubmit')
        .should('have.been.calledOnce');
    });
  });

  describe('Failed', () => {
    describe('Invalid form', () => {
      beforeEach(() => {
        cy.mount(() =>
          h(FormRecipeCreate, {
            onSubmit: cy.spy().as('onSubmit')
          })
        )
          .root()
          .should('not.contain.text', 'Name is required')
          .should('not.contain.text', 'Invalid URL');
      });

      afterEach(() => {
        cy.get('@onSubmit').should('not.have.been.called');
      });

      it('Can not create recipe with empty name', () => {
        cy.get('[data-test=form-recipe-create-submit-button]')
          .click()
          .root()
          .should('contain.text', 'Name is required');
      });

      it('Can not create recipe with invalid url', function () {
        cy.get('[data-test=form-image-input-url]')
          .type('Invalid url')
          .root()
          .should('contain.text', 'Invalid URL');
      });
    });
  });
});

describe('Cancel', () => {
  it('Cancel will emit cancel even', () => {
    cy.mount(() =>
      h(FormRecipeCreate, {
        onCancel: cy.spy().as('onCancel')
      })
    )
      .get('[data-test=form-recipe-create-cancel-button]')
      .click()
      .get('@onCancel')
      .should('have.been.called');
  });
});

describe('Loading', () => {
  describe('No loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('not.exist')
        .get('[data-test=form-recipe-create-name] input')
        .should('not.be.disabled')
        .get('[data-test=form-recipe-create-description] textarea')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('not.be.disabled')
        .get('[data-test=form-recipe-create-submit-button]')
        .should('not.be.disabled')
        .get('[data-test=form-recipe-create-cancel-button]')
        .should('not.be.disabled');
    });

    it('default', () => {
      cy.mount(() => h(FormRecipeCreate));
    });

    it('Loading=false', () => {
      cy.mount(() => h(FormRecipeCreate, { loading: false }));
    });
  });

  describe('Loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('be.visible')
        .get('[data-test=form-recipe-create-name] input')
        .should('be.disabled')
        .get('[data-test=form-recipe-create-description] textarea')
        .should('be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('be.disabled')
        .get('[data-test=form-recipe-create-cancel-button]')
        .should('be.disabled');

      cy.once('fail', (err) => {
        expect(err.message).to.include('`cy.click()` failed because this element');
        expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
      });
      cy.get('[data-test=form-recipe-create-submit-button]').click({ timeout: 100 });
    });

    it('Loading=true', () => {
      cy.mount(() => h(FormRecipeCreate, { loading: true }));
    });
  });
});
