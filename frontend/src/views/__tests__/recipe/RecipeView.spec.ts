import CardRecipe from '@/components/cards/CardRecipe.vue';
import ModalRecipeCreate from '@/components/modals/ModalRecipeCreate.vue';
import { describe, expect, it, vi } from 'vitest';

import { apiUrl } from '@/env';
import { type RecipesResponse } from '@/schema/recipe';
import RecipeView from '@/views/recipe/RecipeView.vue';
import { flushPromises, mount } from '@vue/test-utils';
import axios from 'axios';

import vuetify from '@/components/plugins/vuetify';

vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: () => {}
  }))
}));

describe('RecipeView', () => {
  function factory() {
    return mount(RecipeView, {
      global: {
        plugins: [vuetify]
      }
    });
  }

  const response: RecipesResponse = {
    page: 1,
    total: 2,
    recipes: [
      {
        id: 1,
        name: 'Recipe name 1',
        description: 'Recipe description 1',
        image_uri: 'http://localhost:8080/valid-image-url-1',
        ingredients: []
      },
      {
        id: 2,
        name: 'Recipe name 2',
        description: 'Recipe description 2',
        image_uri: 'http://localhost:8080/valid-image-url-2',
        ingredients: []
      }
    ]
  };

  it('Render result properly', async () => {
    vi.spyOn(axios, 'request').mockResolvedValue({
      data: response
    });

    const wrapper = factory();
    await flushPromises();

    expect(axios.request).toBeCalledTimes(1);
    expect(axios.request).toBeCalledWith({
      method: 'get',
      url: `${apiUrl}/recipes/`
    });

    expect(wrapper.find('[data-test=recipe-view-error]').exists()).toBe(false);
    expect(wrapper.find('[data-test=recipe-view-result]').exists()).toBe(true);
    expect(wrapper.find('[data-test=recipe-view-loading]').exists()).toBe(false);
    expect(wrapper.find('[data-test=recipe-view-new-button]').exists()).toBe(true);

    expect(wrapper.findAllComponents(CardRecipe)).toHaveLength(response.recipes.length);
    expect(wrapper.findComponent(ModalRecipeCreate).exists()).toBe(false);
  });

  it('Render with error', async () => {
    vi.spyOn(axios, 'request').mockImplementation(() => {
      throw new Error('Unexpected error');
    });

    const wrapper = factory();
    await flushPromises();

    expect(wrapper.find('[data-test=recipe-view-error]').text()).toBe('Something wrong ...');
  });

  it('Render with loading', async () => {
    vi.spyOn(axios, 'request').mockResolvedValue({
      data: response
    });

    const wrapper = factory();

    expect(wrapper.find('[data-test=recipe-view-loading]').exists()).toBe(true);
    expect(wrapper.find('[data-test=recipe-view-loading]').text()).toBe('Loading ...');
  });

  it('Click create-new-recipe button', async () => {
    const wrapper = factory();

    const newRecipeButton = wrapper.find('[data-test=recipe-view-new-button]');
    await newRecipeButton.trigger('click');

    expect(wrapper.findComponent(ModalRecipeCreate).exists()).toBe(true);
  });

  it('Click close create-new-recipe modal', async () => {
    const wrapper = factory();

    const newRecipeButton = wrapper.find('[data-test=recipe-view-new-button]');
    await newRecipeButton.trigger('click');

    const modal = wrapper.findComponent(ModalRecipeCreate);
    await modal.find('[data-test=form-recipe-create-close]').trigger('click');

    expect(wrapper.findComponent(ModalRecipeCreate).exists()).toBe(false);
  });
});
