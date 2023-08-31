import { describe, expect, it } from 'vitest';

import FormRecipeCreate from '@/components/forms/FormRecipeCreate.vue';
import { mount } from '@vue/test-utils';

describe('FormRecipeCreate', () => {
  it('Render properly', () => {
    const wrapper = mount(FormRecipeCreate);

    expect(wrapper.find('[data-test=form-recipe-create-title]').text()).toBe('Create New Recipe');
    expect(wrapper.find('[data-test=form-recipe-create-name]').text()).toBe('Name:');
    expect(wrapper.find('[data-test=form-recipe-create-description]').text()).toBe('Description:');
    expect(wrapper.find('[data-test=form-recipe-create-image-uri]').text()).toBe('Image URL:');
  });

  it('Submit form', async () => {
    const wrapper = mount(FormRecipeCreate);

    await wrapper
      .find('[data-test=form-recipe-create-name]')
      .find('input')
      .setValue('Recipe name 1');
    await wrapper
      .find('[data-test=form-recipe-create-description]')
      .find('input')
      .setValue('Recipe description 1');
    await wrapper
      .find('[data-test=form-recipe-create-image-uri]')
      .find('input')
      .setValue('http://localhost/valid-image-url');

    await wrapper.find('form').trigger('submit');
    const submittedEvent = wrapper.emitted('submit');

    expect(submittedEvent).toHaveLength(1);
    // @ts-ignore
    expect(submittedEvent[0]).toStrictEqual([
      {
        name: 'Recipe name 1',
        description: 'Recipe description 1',
        image_uri: 'http://localhost/valid-image-url'
      }
    ]);
  });

  it('Emit close', async () => {
    const wrapper = mount(FormRecipeCreate);

    await wrapper.find('[data-test=form-recipe-create-close]').trigger('click');

    expect(wrapper.emitted('close')).toHaveLength(1);
  });
});
