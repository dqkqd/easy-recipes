import DeleteButton from '@/components/DeleteButton.vue';
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

    .getTestSelector('delete-button-dialog')
    .should('not.exist');
});

it('Render default properly', () => {
  cy.mount(() => h(DeleteButton))
    .root()
    .should('contain', 'mdi-delete');
});

it('Show dialog when clicking delete button', () => {
  cy.mount(() => h(DeleteButton))
    .getTestSelector('delete-button')
    .click()
    .getTestSelector('delete-button-dialog')
    .should('be.visible');
});

it('Close dialog when clicking cancel', () => {
  cy.mount(() => h(DeleteButton))
    .getTestSelector('delete-button')
    .click()

    .getTestSelector('delete-button-dialog')
    .findTestSelector('card-warning-cancel-button')
    .click()

    .getTestSelector('delete-button-dialog')
    .should('not.exist');
});

it('Close dialog when clicking accept', () => {
  cy.mount(() => h(DeleteButton))
    .getTestSelector('delete-button')
    .click()

    .getTestSelector('delete-button-dialog')
    .findTestSelector('card-warning-accept-button')
    .click()

    .getTestSelector('delete-button-dialog')
    .should('not.exist');
});

it('Emit accept event when clicking accept', () => {
  cy.mount(() =>
    h(DeleteButton, {
      onAccept: cy.spy().as('onAccept')
    })
  )
    .getTestSelector('delete-button')
    .click()

    .getTestSelector('delete-button-dialog')
    .findTestSelector('card-warning-accept-button')
    .click()

    .get('@onAccept')
    .should('have.been.calledOnce');
});
