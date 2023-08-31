import { mount } from '@vue/test-utils';
import { describe, expect, it } from 'vitest';

import DeleteButton from '@/components/buttons/DeleteButton.vue';

describe('DeleteButton', () => {
  it('Render properly', () => {
    const wrapper = mount(DeleteButton, {
      props: {
        label: 'Delete button'
      }
    });

    expect(wrapper.find('[data-test=delete-button]').text()).toBe('Delete button');
  });

  it('Emit close', async () => {
    const wrapper = mount(DeleteButton, {
      props: {
        label: 'Delete button'
      }
    });

    await wrapper.find('[data-test=delete-button]').trigger('click');
    expect(wrapper.emitted('close')).toHaveLength(1);
  });
});
