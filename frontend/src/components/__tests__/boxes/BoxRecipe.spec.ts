import { describe, expect, it } from 'vitest';

import BoxRecipe from '@/components/boxes/BoxRecipe.vue';
import { Recipe } from '@/interfaces/recipe';
import { mount } from '@vue/test-utils';

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
});
