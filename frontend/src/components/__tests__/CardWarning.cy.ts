import CardWarning from '@/components/CardWarning.vue';
import { h } from 'vue';

it('Render properly', () => {
  const props = {
    title: 'My card title',
    acceptLabel: 'My accept label',
    cancelLabel: 'My cancel label'
  };

  cy.mount(() => h(CardWarning, props))
    .getTestSelector('card-warning-title')
    .should('have.text', props.title)

    .getTestSelector('card-warning-accept-button')
    .should('have.text', props.acceptLabel)

    .getTestSelector('card-warning-cancel-button')
    .should('have.text', props.cancelLabel);
});

it('Render default', () => {
  cy.mount(() => h(CardWarning))
    .getTestSelector('card-warning-title')
    .should('not.exist')

    .getTestSelector('card-warning-accept-button')
    .should('have.text', 'Accept')

    .getTestSelector('card-warning-cancel-button')
    .should('have.text', 'Cancel');
});

it('Emit accept and cancel when clicking', () => {
  cy.mount(() =>
    h(CardWarning, {
      onAccept: cy.spy().as('onAccept'),
      onCancel: cy.spy().as('onCancel')
    })
  )

    .getTestSelector('card-warning-accept-button')
    .click()
    .get('@onAccept')
    .should('have.been.calledOnce')

    .getTestSelector('card-warning-cancel-button')
    .click()
    .get('@onCancel')
    .should('have.been.calledOnce');
});
