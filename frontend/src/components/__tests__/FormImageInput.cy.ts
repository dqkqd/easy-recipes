import FormImageInput from '@/components/FormImageInput.vue';
import { defaultImage } from '@/env';
import { h } from 'vue';

describe('Render', () => {
  it('Render properly', () => {
    cy.mount(() => h(FormImageInput))
      .getTestSelector('form-image-input-file')
      .find('label')
      .should('have.text', 'Upload your image here, or use urlUpload your image here, or use url')

      .getTestSelector('form-image-input-url')
      .find('label')
      .first()
      .should('have.text', 'Image URL')

      .getTestSelector('form-image-input-image')
      .find('img')
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
      cy.getTestSelector('form-image-input-file').find('input').click();
    });

    it('Hint should be shown on url input click', () => {
      cy.getTestSelector('form-image-input-url').find('input').click();
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
      .getTestSelector('form-image-input-image')
      .find('img')
      .should('have.attr', 'src', defaultImage);
  });

  afterEach(() => {
    cy.getTestSelector('form-image-input-image')
      .find('img')
      .should('not.have.attr', 'src', defaultImage)
      .get('@onUpdate')
      .should('have.been.called');
  });

  it('Select file should display image', () => {
    cy.getTestSelector('form-image-input-file')
      .find('input')
      .selectFile('cypress/fixtures/images/recipe.png');
  });

  it('Input image url should display image', () => {
    cy.fixture('recipes/details/1.json').then((validRecipe) => {
      cy.getTestSelector('form-image-input-url').find('input').type(validRecipe.image_uri);
    });
  });
});

describe('Disable input', () => {
  it('Both inputs are initially enabled', () => {
    cy.mount(() => h(FormImageInput))
      .getTestSelector('form-image-input-url')
      .find('input')
      .should('be.enabled')
      .getTestSelector('form-image-input-file')
      .find('input')
      .should('be.enabled');
  });

  it('URL input is disabled when file is selected', () => {
    cy.mount(() => h(FormImageInput))
      .getTestSelector('form-image-input-file')
      .find('input')
      .selectFile('cypress/fixtures/images/recipe.png')
      .getTestSelector('form-image-input-url')
      .find('input')
      .should('be.disabled');
  });

  it('File input is disable when url input has value', () => {
    cy.fixture('recipes/details/1.json').then((validRecipe) => {
      cy.mount(() => h(FormImageInput))
        .getTestSelector('form-image-input-url')
        .find('input')
        .type(validRecipe.image_uri)
        .getTestSelector('form-image-input-file')
        .find('input')
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
      .getTestSelector('form-image-input-url')
      .find('input')
      .should('be.disabled')
      .getTestSelector('form-image-input-file')
      .find('input')
      .should('be.disabled');
  });
});

describe('Props image', () => {
  beforeEach(() => {
    cy.fixture('recipes/details/1.json')
      .as('recipe')
      .then((recipe) => {
        cy.mount(() =>
          h(FormImageInput, {
            modelValue: null,
            image: recipe.image_uri
          })
        );
      });
  });

  afterEach(function () {
    cy.getTestSelector('form-image-input-image')
      .find('img')
      .should('have.attr', 'src', this.recipe.image_uri);
  });

  it('Render props image when image url is invalid', function () {
    cy.getTestSelector('form-image-input-url').find('input').type('abc');
  });

  it('Render props image when image file is invalid', function () {
    cy.getTestSelector('form-image-input-file')
      .find('input')
      .selectFile('cypress/fixtures/recipes/details/1.json');
  });

  it('Render props image after clearing image url input', function () {
    const image = 'https://picsum.photos/200';
    cy.getTestSelector('form-image-input-url')
      .find('input')
      .type(image)

      .getTestSelector('form-image-input-image')
      .find('img')
      .should('have.attr', 'src', image)

      .getTestSelector('form-image-input-url')
      .find('input')
      .clear();
  });

  it('Render props image after clearing image file input', function () {
    cy.getTestSelector('form-image-input-file')
      .find('input')
      .selectFile('cypress/fixtures/images/recipe.png')

      .getTestSelector('form-image-input-image')
      .find('img')
      .should('not.have.attr', 'src', this.recipe.image_uri)

      .getTestSelector('form-image-input-file')
      .find('i[role=button]')
      .click();
  });
});
