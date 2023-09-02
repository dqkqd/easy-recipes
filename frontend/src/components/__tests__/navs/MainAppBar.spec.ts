import { describe, expect, it, test, vi } from 'vitest';

import MainAppBar from '@/components/navs/MainAppBar.vue';
import vuetify from '@/plugins/vuetify';
import { mount } from '@vue/test-utils';
import { useRouter } from 'vue-router';

describe('MainAppBar', () => {
  vi.mock('vue-router', () => ({
    useRouter: vi.fn(() => ({
      push: () => {}
    }))
  }));

  function factory() {
    return mount(MainAppBar, {
      globals: {
        plugins: [vuetify]
      }
    });
  }

  it('Render properly', () => {
    const wrapper = factory();

    expect(wrapper.find('[data-test=main-app-bar-home-button]').text()).toBe('Easy Recipes');
    expect(wrapper.find('[data-test=main-app-bar-recipes-button]').attributes('text')).toBe(
      'Recipes'
    );
    expect(wrapper.find('[data-test=main-app-bar-ingredients-button]').attributes('text')).toBe(
      'Ingredients'
    );
  });

  test.each`
    selector                                         | page
    ${'[data-test=main-app-bar-home-button]'}        | ${'home'}
    ${'[data-test=main-app-bar-recipes-button]'}     | ${'RecipeView'}
    ${'[data-test=main-app-bar-ingredients-button]'} | ${'IngredientView'}
  `("Move to $page when clicking $page's button", async ({ selector, page }) => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));
    const wrapper = factory();

    const button = wrapper.find(selector);
    await button.trigger('click');

    expect(push).toHaveBeenCalledTimes(1);
    expect(push).toBeCalledWith({ name: page });
  });
});
