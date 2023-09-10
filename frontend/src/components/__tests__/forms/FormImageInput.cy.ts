import FormImageInput from '@/components/forms/FormImageInput.vue';
import { defaultImage } from '@/env';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(FormImageInput))
      .get('[data-test=form-image-input-file] label')
      .should('have.text', 'Upload your image here, or use urlUpload your image here, or use url')

      .get('[data-test=form-image-input-url] label')
      .first()
      .should('have.text', 'Image URL')

      .get('[data-test=form-image-input-image] img')
      .should('have.attr', 'src', defaultImage);
  });

  describe('Hint', () => {
    beforeEach(() => {
      cy.mount(() =>
        h(FormImageInput, {
          modelValue: null,
          hint: 'This is a hint'
        })
      )
        .root()
        .should('not.contain.text', 'This is a hint');
    });

    afterEach(() => {
      cy.root().should('contain.text', 'This is a hint');
    });

    it('Hint should be shown on file input click', () => {
      cy.get('[data-test=form-image-input-file] input').click();
    });

    it('Hint should be shown on url input click', () => {
      cy.get('[data-test=form-image-input-url] input').click();
    });
  });
});

describe('Input image', () => {
  beforeEach(() => {
    cy.mount(() =>
      h(FormImageInput, {
        modelValue: null,
        'onUpdate:modelValue': cy.spy().as('onUpdate')
      })
    )
      .get('[data-test=form-image-input-image] img')
      .should('have.attr', 'src', defaultImage);
  });

  afterEach(() => {
    cy.get('[data-test=form-image-input-image] img')
      .should('not.have.attr', 'src', defaultImage)
      .get('@onUpdate')
      .should('have.been.called');
  });

  it('Select file should display image', () => {
    cy.get('[data-test=form-image-input-file] input').selectFile(
      'cypress/fixtures/images/recipe.png'
    );
  });

  it('Input image url should display image', () => {
    cy.fixture('recipes/details/1.json').then((validRecipe) => {
      cy.get('[data-test=form-image-input-url] input').type(validRecipe.image_uri);
    });
  });
});

describe('Disable input', () => {
  it('Both inputs are initially enabled', () => {
    cy.mount(() => h(FormImageInput))
      .get('[data-test=form-image-input-url] input')
      .should('be.enabled')
      .get('[data-test=form-image-input-file] input')
      .should('be.enabled');
  });

  it('URL input is disabled when file is selected', () => {
    cy.mount(() => h(FormImageInput))
      .get('[data-test=form-image-input-file] input')
      .selectFile('cypress/fixtures/images/recipe.png')
      .get('[data-test=form-image-input-url] input')
      .should('be.disabled');
  });

  it('File input is disable when url input has value', () => {
    cy.fixture('recipes/details/1.json').then((validRecipe) => {
      cy.mount(() => h(FormImageInput))
        .get('[data-test=form-image-input-url] input')
        .type(validRecipe.image_uri)
        .get('[data-test=form-image-input-file] input')
        .should('be.disabled');
    });
  });

  it('Both input are disabled while loading', () => {
    cy.mount(() =>
      h(FormImageInput, {
        modelValue: null,
        loading: true
      })
    )
      .get('[data-test=form-image-input-url] input')
      .should('be.disabled')
      .get('[data-test=form-image-input-file] input')
      .should('be.disabled');
  });
});
