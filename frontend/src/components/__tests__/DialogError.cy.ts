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
      .get('[data-test=dialog-error-title]')
      .should('have.text', 'Error title')
      .get('[data-test=dialog-error-content]')
      .should('have.text', 'Error content');
  });

  it("Don't show title and content", () => {
    cy.mount(() =>
      h(DialogError, {
        modelValue: true
      })
    )
      .get('[data-test=dialog-error-title]')
      .should('not.exist')
      .get('[data-test=dialog-error-content]')
      .should('not.exist');
  });
});
