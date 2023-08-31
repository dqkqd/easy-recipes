import { describe, expect, it, vi } from 'vitest';

import BoxRecipe from '@/components/boxes/BoxRecipe.vue';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { mount } from '@vue/test-utils';
import { useRouter } from 'vue-router';

vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: () => {}
  }))
}));

describe('BoxRecipe', () => {
  function boxRecipeFactory(recipe: Recipe) {
    return mount(BoxRecipe, {
      props: { recipe: RecipeSchema.parse(recipe) }
    });
  }

  it('Render properly', () => {
    const wrapper = boxRecipeFactory({
      id: 1,
      name: 'Recipe name',
      description: 'Recipe Description',
      image_uri: 'http://localhost/valid-image-url',
      ingredients: []
    });

    expect(wrapper.find('[data-test=box-recipe-name]').text()).toBe('Recipe name');
    expect(wrapper.find('[data-test=box-recipe-description]').text()).toBe('Recipe Description');
    expect(wrapper.find('[data-test=box-recipe-valid-image]').attributes('src')).toBe(
      'http://localhost/valid-image-url'
    );
  });

  it('Do not show empty description', async () => {
    const wrapper = boxRecipeFactory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    expect(wrapper.find('[data-test=box-recipe-description]').exists()).toBe(false);

    await wrapper.setProps({
      recipe: {
        id: 1,
        name: 'Recipe name',
        description: '',
        image_uri: null,
        ingredients: []
      }
    });

    expect(wrapper.find('[data-test=box-recipe-description]').exists()).toBe(false);
  });

  it('Render default image if no specify', () => {
    const wrapper = boxRecipeFactory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    expect(wrapper.find('[data-test=box-recipe-default-image]').attributes('src')).toBe(
      '/no-image-icon.png'
    );
  });

  it('Move to recipe details when click', async () => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));

    const wrapper = boxRecipeFactory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    await wrapper.trigger('click');

    expect(push).toHaveBeenCalledTimes(1);
    expect(push).toBeCalledWith({ name: 'RecipeDetails', params: { id: 1 } });
  });
});
