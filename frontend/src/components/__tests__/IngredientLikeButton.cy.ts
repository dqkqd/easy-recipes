import IngredientLikeButton from '@/components/IngredientLikeButton.vue';
import { apiUrl } from '@/env';
import { h } from 'vue';

describe('Render', () => {
  afterEach(() => {
    cy.getTestSelector('ingredient-like-button-icon').should('be.visible');
  });

  it('No one like this ingredient', () => {
    cy.fixture('ingredients/like/no-like.json').then((ingredient) => {
      cy.mount(() => h(IngredientLikeButton, { ingredient }))
        .getTestSelector('ingredient-like-button-text')
        .should('have.text', 'Be the first to like this');
    });
  });

  it('Someone like this ingredient', () => {
    cy.fixture('ingredients/like/12-likes.json').then((ingredient) => {
      cy.mount(() => h(IngredientLikeButton, { ingredient }))
        .getTestSelector('ingredient-like-button-text')
        .should('have.text', '12 people like this');
    });
  });
});

describe('Click like button', () => {
  it('Should increase total likes', () => {
    cy.fixture('ingredients/like/12-likes.json').then((ingredient) => {
      cy.intercept(
        { method: 'post', url: `${apiUrl}/ingredients/${ingredient.id}/like` },
        { id: ingredient.id, total_likes: ingredient.likes + 1 }
      );

      cy.mount(() => h(IngredientLikeButton, { ingredient }))
        .getTestSelector('ingredient-like-button-text')
        .should('have.text', '12 people like this')

        .getTestSelector('ingredient-like-button-icon')
        .click()

        .getTestSelector('ingredient-like-button-text')
        .should('have.text', '13 people like this');
    });
  });

  it('Should loading', () => {
    cy.fixture('ingredients/like/no-like.json').then((ingredient) => {
      cy.intercept(
        { method: 'post', url: `${apiUrl}/ingredients/${ingredient.id}/like` },
        { delay: 1000 }
      );

      cy.mount(() => h(IngredientLikeButton, { ingredient }))
        .getTestSelector('ingredient-like-button-icon')
        .click()
        .getTestSelector('ingredient-like-button-icon')
        .should('be.disabled');
    });
  });
});
