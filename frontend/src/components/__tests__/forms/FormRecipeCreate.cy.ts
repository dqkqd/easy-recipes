import FormRecipeCreate from '@/components/forms/FormRecipeCreate.vue';
import { h } from 'vue';

describe('Render', () => {
  it.only('Render properly', () => {
    cy.mount(() => h(FormRecipeCreate, { loading: false }))

      .get('[data-test="form-recipe-create-name"] label')
      .first()
      .should('have.text', 'Name *')

      .get('[data-test="form-recipe-create-description"] label')
      .first()
      .should('have.text', 'Description')

      .get('[data-test="form-recipe-create-submit-button"]')
      .should('have.text', 'Submit')

      .get('[data-test="form-recipe-create-cancel-button"]')
      .should('have.text', 'Cancel');
  });
});

describe('Submission', () => {
  before(() => {
    cy.wrap({
      name: 'valid name',
      imageUri: 'http://example.com',
      description: 'valid description'
    }).as('validForm');
  });

  describe('Failed submission', () => {
    beforeEach(() => {
      cy.mount(() =>
        h(FormRecipeCreate, {
          loading: false,
          onSubmit: cy.spy().as('onSubmit')
        })
      );
    });

    it('Can not create recipe with empty name', function () {
      cy.get('[data-test="form-recipe-image-uri"] input')
        .type(this.validForm.imageUri)
        .get('[data-test="form-recipe-description"] textarea')
        .type(this.validForm.description)

        .get('[class=v-form]')
        .should('not.contain.text', 'Name is required')

        .get('[data-test="form-recipe-submit-button"]')
        .click()

        .get('[class=v-form]')
        .should('contain.text', 'Name is required')

        .get('@onSubmit')
        .should('not.have.been.called');
    });

    it('Can not create recipe with empty url', function () {
      cy.get('[data-test="form-recipe-name"] input')
        .type(this.validForm.name)
        .get('[data-test="form-recipe-description"] textarea')
        .type(this.validForm.description)

        .get('[class=v-form]')
        .should('not.contain.text', 'Invalid URL')

        .get('[data-test="form-recipe-submit-button"]')
        .click()

        .get('[class=v-form]')
        .should('contain.text', 'Invalid URL')

        .get('@onSubmit')
        .should('not.have.been.called');
    });

    it('Can not create recipe with invalid url', function () {
      cy.get('[data-test="form-recipe-name"] input')
        .type(this.validForm.name)
        .get('[data-test="form-recipe-image-uri"] input')
        .type('this is invalid url')
        .get('[data-test="form-recipe-description"] textarea')
        .type(this.validForm.description)

        .get('[class=v-form]')
        .should('contain.text', 'Invalid URL')

        .get('[data-test="form-recipe-submit-button"]')
        .click()

        .get('@onSubmit')
        .should('not.have.been.called');
    });
  });

  describe('Successful submission', () => {
    it('Submit without error', function () {
      cy.mount(() =>
        h(FormRecipeCreate, {
          loading: false,
          onSubmit: cy.spy().as('onSubmit')
        })
      )
        .get('[data-test="form-recipe-name"] input')
        .type(this.validForm.name)
        .get('[data-test="form-recipe-image-uri"] input')
        .type(this.validForm.imageUri)
        .get('[data-test="form-recipe-description"] textarea')
        .type(this.validForm.description)

        .get('[data-test=form-recipe-submit-button]')
        .click()

        .get('@onSubmit')
        .should(
          'have.been.calledOnceWith',
          this.validForm.name,
          this.validForm.imageUri,
          this.validForm.description
        );
    });
  });
});

describe('Successfully cancel', () => {
  it('Cancel without error', function () {
    cy.mount(() =>
      h(FormRecipeCreate, {
        loading: false,
        onCancel: cy.spy().as('onCancel')
      })
    )
      .get('[data-test=form-recipe-cancel-button]')
      .click()

      .get('@onCancel')
      .should('have.been.calledOnce');
  });
});

describe('Loading', () => {
  it('Form disabled while loading', function () {
    cy.mount(() =>
      h(FormRecipeCreate, {
        loading: true
      })
    )

      .get('.v-progress-circular')
      .should('exist')

      .get('[data-test=form-recipe-name] input')
      .should('be.disabled')

      .get('[data-test=form-recipe-image-uri] input')
      .should('be.disabled')

      .get('[data-test=form-recipe-description] textarea')
      .should('be.disabled')

      .get('[data-test=form-recipe-cancel-button]')
      .should('be.disabled');

    cy.once('fail', (err) => {
      expect(err.message).to.include('`cy.click()` failed because this element');
      expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
    });
    cy.get('[data-test=form-recipe-submit-button]').click({ timeout: 100 });
  });

  it('Form available with no loading passed', () => {
    cy.mount(() => h(FormRecipeCreate))

      .get('[data-test=form-recipe-name] input')
      .should('not.be.disabled')

      .get('[data-test=form-recipe-image-uri] input')
      .should('not.be.disabled')

      .get('[data-test=form-recipe-description] textarea')
      .should('not.be.disabled')

      .get('[data-test=form-recipe-cancel-button]')
      .should('not.be.disabled')

      .get('[data-test=form-recipe-submit-button]')
      .click();
  });
});
