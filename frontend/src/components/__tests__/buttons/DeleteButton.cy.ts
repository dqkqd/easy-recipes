import DeleteButton from '@/components/buttons/DeleteButton.vue';
import { h } from 'vue';

it('Render properly', () => {
  cy.mount(() =>
    h(DeleteButton, {
      icon: 'mdi-plus',
      title: 'You want to delete it?'
    })
  )
    .root()
    .should('contain', 'mdi-plus')

    .get('[data-test=delete-button-dialog]')
    .should('not.exist');
});

it('Render default properly', () => {
  cy.mount(() => h(DeleteButton))
    .root()
    .should('contain', 'mdi-delete');
});

it('Show dialog when clicking delete button', () => {
  cy.mount(() => h(DeleteButton))
    .get('[data-test=delete-button]')
    .click()
    .get('[data-test=delete-button-dialog]')
    .should('be.visible');
});

it('Close dialog when clicking cancel', () => {
  cy.mount(() => h(DeleteButton))
    .get('[data-test=delete-button]')
    .click()

    .get('[data-test=delete-button-dialog] [data-test=card-warning-cancel-button]')
    .click()

    .get('[data-test=delete-button-dialog]')
    .should('not.exist');
});

it('Close dialog when clicking accept', () => {
  cy.mount(() => h(DeleteButton))
    .get('[data-test=delete-button]')
    .click()

    .get('[data-test=delete-button-dialog] [data-test=card-warning-accept-button]')
    .click()

    .get('[data-test=delete-button-dialog]')
    .should('not.exist');
});

it('Emit accept event when clicking accept', () => {
  cy.mount(() =>
    h(DeleteButton, {
      onAccept: cy.spy().as('onAccept')
    })
  )
    .get('[data-test=delete-button]')
    .click()

    .get('[data-test=delete-button-dialog] [data-test=card-warning-accept-button]')
    .click()

    .get('@onAccept')
    .should('have.been.calledOnce');
});
