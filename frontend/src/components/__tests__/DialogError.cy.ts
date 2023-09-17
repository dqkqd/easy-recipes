import DialogError from '@/components/DialogError.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render default', () => {
    cy.mount(() =>
      h(DialogError, {
        modelValue: true,
        title: 'Error title',
        content: 'Error content'
      })
    )
      .getTestSelector('dialog-error-title')
      .should('have.text', 'Error title')
      .getTestSelector('dialog-error-content')
      .should('have.text', 'Error content');
  });

  it("Don't show title and content", () => {
    cy.mount(() =>
      h(DialogError, {
        modelValue: true
      })
    )
      .getTestSelector('dialog-error-title')
      .should('not.exist')
      .getTestSelector('dialog-error-content')
      .should('not.exist');
  });
});
