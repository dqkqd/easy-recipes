import BaseViewBanner from '@/components/BaseViewBanner.vue';
import { h } from 'vue';

beforeEach(() => {});

describe('Render', () => {
  it('With button', () => {
    cy.mount(() =>
      h(BaseViewBanner, {
        bannerImage: 'https://picsum.photos/200',
        bannerTitle: 'Banner Title',
        buttonLabel: 'Button Label'
      })
    )
      .get('[data-test=base-view-banner-image] img')
      .should('have.attr', 'src', 'https://picsum.photos/200')

      .get('[data-test=base-view-banner-title]')
      .should('contain.text', 'Banner Title')

      .get('[data-test=base-view-banner-button]')
      .should('be.visible');
  });

  it('Without button', () => {
    cy.mount(() =>
      h(BaseViewBanner, {
        bannerImage: 'https://picsum.photos/200',
        bannerTitle: 'Banner Title'
      })
    )

      .get('[data-test=base-view-banner-button]')
      .should('not.exist');
  });
});
