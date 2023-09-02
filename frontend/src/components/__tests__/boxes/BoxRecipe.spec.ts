import { describe, expect, it, vi } from 'vitest';

import BoxRecipe from '@/components/boxes/BoxRecipe.vue';
import vuetify from '@/components/plugins/vuetify';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { mount } from '@vue/test-utils';
import { useRouter } from 'vue-router';

vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: () => {}
  }))
}));

describe('BoxRecipe', () => {
  function factory(recipe: Recipe) {
    return mount(BoxRecipe, {
      props: { recipe: RecipeSchema.parse(recipe) },
      globals: {
        plugins: [vuetify]
      }
    });
  }

  it('Render properly', () => {
    const wrapper = factory({
      id: 1,
      name: 'Recipe name',
      description: 'Recipe Description',
      image_uri: 'http://localhost/valid-image-url',
      ingredients: []
    });

    expect(wrapper.find('[data-test=box-recipe-name]').text()).toBe('Recipe name');
    expect(wrapper.find('[data-test=box-recipe-description]').text()).toBe('Recipe Description');
    expect(wrapper.find('[data-test=box-recipe-image]').attributes('src')).toBe(
      'http://localhost/valid-image-url'
    );
  });

  it('Empty description should be shown as `No description`', async () => {
    const wrapper = factory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    expect(wrapper.find('[data-test=box-recipe-description]').text()).toBe('No description');

    await wrapper.setProps({
      recipe: {
        id: 1,
        name: 'Recipe name',
        description: null,
        image_uri: null,
        ingredients: []
      }
    });

    expect(wrapper.find('[data-test=box-recipe-description]').text()).toBe('No description');
  });

  it('Render default image if no specify', () => {
    const wrapper = factory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    expect(wrapper.find('[data-test=box-recipe-image]').attributes('src')).toBe(
      '/no-image-icon.png'
    );
  });

  it('Move to recipe details when click', async () => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));

    const wrapper = factory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    const moveButton = wrapper.find('[data-test=box-recipe-to-recipe-details-button]');
    await moveButton.trigger('click');

    expect(push).toHaveBeenCalledTimes(1);
    expect(push).toBeCalledWith({ name: 'RecipeDetails', params: { id: 1 } });
  });
});
