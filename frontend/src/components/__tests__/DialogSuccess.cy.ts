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
      .get('[data-test=dialog-success-title]')
      .should('have.text', 'Success title')
      .get('[data-test=dialog-success-content]')
      .should('have.text', 'Success content');
  });

  it("Don't show title and content", () => {
    cy.mount(() =>
      h(DialogSuccess, {
        modelValue: true
      })
    )
      .get('[data-test=dialog-success-title]')
      .should('not.exist')
      .get('[data-test=dialog-success-content]')
      .should('not.exist');
  });
});
