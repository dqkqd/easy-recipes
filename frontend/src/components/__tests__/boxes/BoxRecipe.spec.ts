import { describe, expect, it, vi } from 'vitest';

import BoxRecipe from '@/components/boxes/BoxRecipe.vue';
import { Recipe } from '@/interfaces/recipe';
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
      props: { recipe: recipe }
    });
  }

  it('Render properly', () => {
    const wrapper = boxRecipeFactory(
      new Recipe(1, 'Recipe name', 'Recipe Description', 'Sample image', [])
    );

    expect(wrapper.find('[class=name]').text()).toBe('Recipe name');
    expect(wrapper.find('[class=description]').text()).toBe('Recipe Description');
    expect(wrapper.find('[class=recipe-image]').attributes('src')).toBe('Sample image');
  });

  it('Do not show empty description', async () => {
    const wrapper = boxRecipeFactory(new Recipe(1, 'Recipe name', '', null, []));

    expect(wrapper.find('[class=description]').exists()).toBe(false);

    await wrapper.setProps({ recipe: new Recipe(1, 'Recipe name', null, null, []) });

    expect(wrapper.find('[class=description]').exists()).toBe(false);
  });

  it('Render default image if no specify', () => {
    const wrapper = boxRecipeFactory(new Recipe(1, 'Recipe name', 'Recipe Description', null, []));

    expect(wrapper.find('[class=recipe-image]').attributes('src')).toBe('/no-image-icon.png');
  });

  it('Move to recipe details when click', async () => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));

    const wrapper = boxRecipeFactory(new Recipe(1, 'Recipe name', null, null, []));

    await wrapper.find('[class=box]').trigger('click');

    expect(push).toHaveBeenCalledTimes(1);
    expect(push).toBeCalledWith({ name: 'RecipeDetails', params: { id: 1 } });
  });
});
