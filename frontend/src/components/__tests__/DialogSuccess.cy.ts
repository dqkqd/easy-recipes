import DialogSuccess from '@/components/DialogSuccess.vue';
import { h } from 'vue';

describe('Render', () => {
  it('Render default', () => {
    cy.mount(() =>
      h(DialogSuccess, {
        modelValue: true,
        title: 'Success title',
        content: 'Success content'
      })
    )
      .getTestSelector('dialog-success-title')
      .should('have.text', 'Success title')
      .getTestSelector('dialog-success-content')
      .should('have.text', 'Success content');
  });

  it("Don't show title and content", () => {
    cy.mount(() =>
      h(DialogSuccess, {
        modelValue: true
      })
    )
      .getTestSelector('dialog-success-title')
      .should('not.exist')
      .getTestSelector('dialog-success-content')
      .should('not.exist');
  });
});
