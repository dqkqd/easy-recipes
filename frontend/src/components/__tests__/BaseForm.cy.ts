import BaseForm from '@/components/BaseForm.vue';
import { h } from 'vue';

before(() => {
  cy.wrap({
    name: 'Form name',
    description: 'Form description',
    image: 'https://picsum.photos/200'
  }).as('form');
});

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(BaseForm))

      .getTestSelector('base-form-name')
      .find('label')
      .first()
      .should('have.text', 'Name *')

      .getTestSelector('base-form-description')
      .find('label')
      .first()
      .should('have.text', 'Description')

      .getTestSelector('base-form-submit-button')
      .should('have.text', 'Submit');
  });

  it('Render passed props', function () {
    cy.mount(() =>
      h(BaseForm, {
        name: this.form.name,
        description: this.form.description,
        image: this.form.image
      })
    )
      .getTestSelector('base-form-name')
      .find('input')
      .should('have.value', this.form.name)

      .getTestSelector('base-form-description')
      .find('textarea')
      .should('have.value', this.form.description)

      .getTestSelector('form-image-input-image')
      .find('img')
      .should('have.attr', 'src', this.form.image);
  });
});

describe('Submit', () => {
  describe('Success', () => {
    beforeEach(function () {
      cy.mount(() =>
        h(BaseForm, {
          onSubmit: cy.spy().as('onSubmit')
        })
      )
        .getTestSelector('base-form-name')
        .type(this.form.name)
        .getTestSelector('base-form-description')
        .type(this.form.description);
    });

    it('No image selected', function () {
      cy.getTestSelector('base-form-submit-button')
        .click()
        .get('@onSubmit')
        .should('have.been.calledWith', this.form.name, null, this.form.description);
    });

    it('Input image url', function () {
      cy.getTestSelector('form-image-input-url')
        .type(this.form.image)
        .getTestSelector('base-form-submit-button')
        .click()
        .get('@onSubmit')
        .should('have.been.calledWith', this.form.name, this.form.image, this.form.description);
    });

    it('Input image file', function () {
      const file = 'cypress/fixtures/images/recipe.png';
      cy.getTestSelector('form-image-input-file')
        .find('input')
        .selectFile(file)
        .getTestSelector('base-form-submit-button')
        .click()
        .get('@onSubmit')
        .should('have.been.calledOnce');
    });
  });

  describe('Failed', () => {
    describe('Invalid form', () => {
      beforeEach(() => {
        cy.mount(() =>
          h(BaseForm, {
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

      it('Can not submit form with empty name', () => {
        cy.getTestSelector('base-form-submit-button')
          .click()
          .root()
          .should('contain.text', 'Name is required');
      });

      it('Can not submit form with invalid url', function () {
        cy.getTestSelector('form-image-input-url')
          .type('Invalid url')
          .root()
          .should('contain.text', 'Invalid URL');
      });
    });
  });
});

describe('Loading', () => {
  describe('No loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('not.exist')
        .getTestSelector('base-form-name')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('base-form-description')
        .find('textarea')
        .should('not.be.disabled')
        .getTestSelector('form-image-input-file')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('form-image-input-url')
        .find('input')
        .should('not.be.disabled')
        .getTestSelector('base-form-submit-button')
        .should('not.be.disabled');
    });

    it('default', () => {
      cy.mount(() => h(BaseForm));
    });

    it('Loading=false', () => {
      cy.mount(() => h(BaseForm, { loading: false }));
    });
  });

  describe('Loading', () => {
    afterEach(() => {
      cy.get('.v-progress-circular')
        .should('be.visible')
        .getTestSelector('base-form-name')
        .find('input')
        .should('be.disabled')
        .getTestSelector('base-form-description')
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
      cy.getTestSelector('base-form-submit-button').click({ timeout: 100 });
    });

    it('Loading=true', () => {
      cy.mount(() => h(BaseForm, { loading: true }));
    });
  });
});
