import CardError from '@/components/cards/CardError.vue';
import { h } from 'vue';

it('Render properly', () => {
  cy.mount(() =>
    h(CardError, null, {
      'error-message': () => 'My error message'
    })
  )

    .get('[data-test=card-error-text]')
    .should('have.text', 'My error message');
});
