import { describe, expect, it } from 'vitest';

import FormInput from '@/components/forms/FormInput.vue';
import FormRecipeCreate from '@/components/forms/FormRecipeCreate.vue';
import { RecipeCreate } from '@/interfaces/recipe';
import { mount } from '@vue/test-utils';

describe('FormRecipeCreate', () => {
  it('Render title', () => {
    const wrapper = mount(FormRecipeCreate);

    const label = wrapper.find('h3');
    expect(label.text()).toBe('Create New Recipe');
  });

  it('Render form', () => {
    const wrapper = mount(FormRecipeCreate);

    const formInputs = wrapper.findAllComponents(FormInput);
    expect(formInputs).toHaveLength(3);

    expect(formInputs[0].find('label').text()).toBe('Name:');
    expect(formInputs[1].find('label').text()).toBe('Description:');
    expect(formInputs[2].find('label').text()).toBe('Image URL:');
  });

  it('Submit form', async () => {
    const wrapper = mount(FormRecipeCreate);

    const formInputs = wrapper.findAllComponents(FormInput);

    const name = formInputs[0].find('input');
    const description = formInputs[1].find('input');
    const imageUrl = formInputs[2].find('input');
    await name.setValue('Recipe name 1');
    await description.setValue('Recipe description 1');
    await imageUrl.setValue('Recipe image url 1');

    await wrapper.find('form').trigger('submit');
    const submittedEvent = wrapper.emitted('submit');

    expect(submittedEvent).toHaveLength(1);
    // @ts-ignore
    expect(submittedEvent[0]).toStrictEqual([
      new RecipeCreate('Recipe name 1', 'Recipe description 1', 'Recipe image url 1')
    ]);
  });

  it('Close form', async () => {
    const wrapper = mount(FormRecipeCreate);

    const closeButton = wrapper.get('button:not([type=submit])');
    await closeButton.trigger('click');
    const closeEvent = wrapper.emitted('close');

    expect(closeEvent).toHaveLength(1);
  });
});
