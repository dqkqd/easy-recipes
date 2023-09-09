import CardWarning from '@/components/cards/CardWarning.vue';
import { h } from 'vue';

it('Render properly', () => {
  const props = {
    title: 'My card title',
    acceptLabel: 'My accept label',
    cancelLabel: 'My cancel label'
  };

  cy.mount(() => h(CardWarning, props))
    .get('[data-test=card-warning-title]')
    .should('have.text', props.title)

    .get('[data-test=card-warning-accept-button]')
    .should('have.text', props.acceptLabel)

    .get('[data-test=card-warning-cancel-button]')
    .should('have.text', props.cancelLabel);
});

it('Render default', () => {
  cy.mount(() => h(CardWarning))
    .get('[data-test=card-warning-title]')
    .should('not.exist')

    .get('[data-test=card-warning-accept-button]')
    .should('have.text', 'Accept')

    .get('[data-test=card-warning-cancel-button]')
    .should('have.text', 'Cancel');
});

it('Emit accept and cancel when clicking', () => {
  cy.mount(() =>
    h(CardWarning, {
      onAccept: cy.spy().as('onAccept'),
      onCancel: cy.spy().as('onCancel')
    })
  )

    .get('[data-test=card-warning-accept-button]')
    .click()
    .get('@onAccept')
    .should('have.been.calledOnce')

    .get('[data-test=card-warning-cancel-button]')
    .click()
    .get('@onCancel')
    .should('have.been.calledOnce');
});
