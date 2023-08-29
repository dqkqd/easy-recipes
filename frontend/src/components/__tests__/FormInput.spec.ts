import { describe, expect, it } from 'vitest';

import { mount } from '@vue/test-utils';
import FormInput from '../forms/FormInput.vue';

describe('FormInput', () => {
  it('Render correctly', async () => {
    const wrapper = mount(FormInput, {
      props: { label: 'test-label', placeholder: 'test place holder', modelValue: '' }
    });

    expect(wrapper.find('label').text()).toBe('test-label:');
    expect(wrapper.find('input').attributes('placeholder')).toBe('test place holder');
  });

  it('Set input value', async () => {
    const wrapper = mount(FormInput, {
      props: { label: '', placeholder: '', modelValue: '' }
    });

    const input = wrapper.find('input');
    await input.setValue('value1');

    expect(input.element.value).toBe('value1');
  });
});
