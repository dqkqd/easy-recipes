import RecipeLikeButton from '@/components/RecipeLikeButton.vue';
import { apiUrl } from '@/env';
import { h } from 'vue';

describe('Render', () => {
  afterEach(() => {
    cy.getTestSelector('recipe-like-button-icon').should('be.visible');
  });

  it('No one like this recipe', () => {
    cy.fixture('recipes/like/no-like.json').then((recipe) => {
      cy.mount(() => h(RecipeLikeButton, { recipe: recipe }))
        .getTestSelector('recipe-like-button-text')
        .should('have.text', 'Be the first to like this');
    });
  });

  it('Someone like this recipe', () => {
    cy.fixture('recipes/like/12-likes.json').then((recipe) => {
      cy.mount(() => h(RecipeLikeButton, { recipe: recipe }))
        .getTestSelector('recipe-like-button-text')
        .should('have.text', '12 people like this');
    });
  });
});

describe('Click like button', () => {
  it('Should increase total likes', () => {
    cy.fixture('recipes/like/12-likes.json').then((recipe) => {
      cy.intercept(
        { method: 'post', url: `${apiUrl}/recipes/${recipe.id}/like` },
        { id: recipe.id, total_likes: recipe.likes + 1 }
      );

      cy.mount(() => h(RecipeLikeButton, { recipe: recipe }))
        .getTestSelector('recipe-like-button-text')
        .should('have.text', '12 people like this')

        .getTestSelector('recipe-like-button-icon')
        .click()

        .getTestSelector('recipe-like-button-text')
        .should('have.text', '13 people like this');
    });
  });

  it('Should loading', () => {
    cy.fixture('recipes/like/no-like.json').then((recipe) => {
      cy.intercept({ method: 'post', url: `${apiUrl}/recipes/${recipe.id}/like` }, { delay: 1000 });

      cy.mount(() => h(RecipeLikeButton, { recipe: recipe }))
        .getTestSelector('recipe-like-button-icon')
        .click()
        .getTestSelector('recipe-like-button-icon')
        .should('be.disabled');
    });
  });
});
