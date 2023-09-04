import CardError from '@/components/cards/CardError.vue';

it('Render properly', () => {
  cy.mount(CardError, { slots: { 'error-message': 'My error message' } })

    .get('[data-test=card-error-text]')
    .should('have.text', 'My error message');
});
