import { describe, expect, it } from 'vitest';

import { mount } from '@vue/test-utils';
import FormInput from '../forms/FormInput.vue';

describe('FormInput', () => {
  it('Render label and input', () => {
    const wrapper = mount(FormInput, { props: { label: 'label1', modelValue: 'value1' } });

    const label = wrapper.find('label');
    const input = wrapper.find('input');

    expect(label.element.textContent).toBe('label1:');
    expect(input.element.value).toBe('value1');
  });

  it('Set the input value', async () => {
    const wrapper = mount(FormInput);

    const input = wrapper.find('input');
    await input.setValue('value1');

    expect(input.element.value).toBe('value1');
  });
});
