import { describe, expect, it, vi } from 'vitest';

import CardRecipe from '@/components/cards/CardRecipe.vue';
import vuetify from '@/components/plugins/vuetify';
import { RecipeSchema, type Recipe } from '@/schema/recipe';
import { mount } from '@vue/test-utils';
import { useRouter } from 'vue-router';

vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: () => {}
  }))
}));

describe('CardRecipe', () => {
  function factory(recipe: Recipe) {
    return mount(CardRecipe, {
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

    expect(wrapper.find('[data-test=card-recipe-name]').text()).toBe('Recipe name');
    expect(wrapper.find('[data-test=card-recipe-image]').attributes('src')).toBe(
      'http://localhost/valid-image-url'
    );
  });

  it('Render default image if no specify', () => {
    const wrapper = factory({
      id: 1,
      name: 'Recipe name',
      description: '',
      image_uri: null,
      ingredients: []
    });

    expect(wrapper.find('[data-test=card-recipe-image]').attributes('src')).toBe(
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

    const moveButton = wrapper.find('[data-test=card-to-recipe-details]');
    await moveButton.trigger('click');

    expect(push).toHaveBeenCalledTimes(1);
    expect(push).toBeCalledWith({ name: 'RecipeDetails', params: { id: 1 } });
  });
});
