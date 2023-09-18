import { stripText } from '@/utils';
import { h } from 'vue';
import RecipeIngredientsDialogSelectCard from '../RecipeIngredientsDialogSelectCard.vue';

beforeEach(() => {
  cy.wrap({
    ingredientName: 'My first ingredient',
    ingredientImage: 'https://picsum.photos/150'
  }).as('basicProps');
});

describe('Render', () => {
  afterEach(function () {
    cy.getTestSelector('recipe-ingredients-dialog-select-card-image')
      .find('img')
      .should('have.attr', 'src', this.basicProps.ingredientImage)
      .getTestSelector('recipe-ingredients-dialog-select-card-name')
      .should('have.text', stripText(this.basicProps.ingredientName, 10));
  });

  it('Render without selected', function () {
    cy.mount(() =>
      h(RecipeIngredientsDialogSelectCard, {
        ...this.basicProps,
        selected: false
      })
    )
      .getTestSelector('recipe-ingredients-dialog-select-card')
      .should('not.have.class', 'selected')
      .getTestSelector('recipe-ingredients-dialog-select-selected-icon')
      .should('not.exist');
  });

  it('Render with selected', function () {
    cy.mount(() =>
      h(RecipeIngredientsDialogSelectCard, {
        ...this.basicProps,
        selected: true
      })
    )
      .getTestSelector('recipe-ingredients-dialog-select-card')
      .should('have.class', 'selected')
      .getTestSelector('recipe-ingredients-dialog-select-selected-icon')
      .should('be.visible');
  });
});

it('Click card emit toggleSelect event', function () {
  cy.mount(() =>
    h(RecipeIngredientsDialogSelectCard, {
      ...this.basicProps,
      selected: true,
      onToggleSelect: cy.spy().as('onToggleSelect')
    })
  )
    .getTestSelector('recipe-ingredients-dialog-select-card')
    .click()
    .get('@onToggleSelect')
    .should('have.been.calledOnce');
});
