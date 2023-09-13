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

      .get('[data-test=base-form-name] label')
      .first()
      .should('have.text', 'Name *')

      .get('[data-test=base-form-description] label')
      .first()
      .should('have.text', 'Description')

      .get('[data-test=base-form-submit-button]')
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
      .get('[data-test=base-form-name] input')
      .should('have.value', this.form.name)

      .get('[data-test=base-form-description] textarea')
      .should('have.value', this.form.description)

      .get('[data-test=form-image-input-image] img')
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
        .get('[data-test=base-form-name]')
        .type(this.form.name)
        .get('[data-test=base-form-description]')
        .type(this.form.description);
    });

    it('No image selected', function () {
      cy.get('[data-test=base-form-submit-button]')
        .click()
        .get('@onSubmit')
        .should('have.been.calledWith', this.form.name, null, this.form.description);
    });

    it('Input image url', function () {
      cy.get('[data-test=form-image-input-url]')
        .type(this.form.image)
        .get('[data-test=base-form-submit-button]')
        .click()
        .get('@onSubmit')
        .should('have.been.calledWith', this.form.name, this.form.image, this.form.description);
    });

    it('Input image file', function () {
      const file = 'cypress/fixtures/images/recipe.png';
      cy.get('[data-test=form-image-input-file] input')
        .selectFile(file)
        .get('[data-test=base-form-submit-button]')
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
        cy.get('[data-test=base-form-submit-button]')
          .click()
          .root()
          .should('contain.text', 'Name is required');
      });

      it('Can not submit form with invalid url', function () {
        cy.get('[data-test=form-image-input-url]')
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
        .get('[data-test=base-form-name] input')
        .should('not.be.disabled')
        .get('[data-test=base-form-description] textarea')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('not.be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('not.be.disabled')
        .get('[data-test=base-form-submit-button]')
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
        .get('[data-test=base-form-name] input')
        .should('be.disabled')
        .get('[data-test=base-form-description] textarea')
        .should('be.disabled')
        .get('[data-test=form-image-input-file] input')
        .should('be.disabled')
        .get('[data-test=form-image-input-url] input')
        .should('be.disabled');

      cy.once('fail', (err) => {
        expect(err.message).to.include('`cy.click()` failed because this element');
        expect(err.message).to.include('`pointer-events: none` prevents user mouse interaction');
      });
      cy.get('[data-test=base-form-submit-button]').click({ timeout: 100 });
    });

    it('Loading=true', () => {
      cy.mount(() => h(BaseForm, { loading: true }));
    });
  });
});
