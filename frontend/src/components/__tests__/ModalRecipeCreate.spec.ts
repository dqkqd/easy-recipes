import { describe, expect, it, vi } from 'vitest';

import { flushPromises, mount } from '@vue/test-utils';
import axios from 'axios';
import { useRouter } from 'vue-router';
import ModalRecipeCreate from '../modals/ModalRecipeCreate.vue';

vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: () => {}
  }))
}));

describe('ModalRecipeCreate', () => {
  it('Emit close', async () => {
    const wrapper = mount(ModalRecipeCreate);

    const closeButton = wrapper.findAll('button')[1];
    await closeButton.trigger('click');

    expect(wrapper.emitted('close')).toHaveLength(1);
  });

  it('Create recipe successfully', async () => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));

    const wrapper = mount(ModalRecipeCreate);

    vi.spyOn(axios, 'post').mockResolvedValue({
      data: { id: 1, error: undefined }
    });

    const inputs = wrapper.findAll('input');
    await inputs[0].setValue('one');
    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(push).toHaveBeenCalledTimes(1);
    expect(push).toBeCalledWith({ name: 'RecipeDetails', params: { id: 1 } });
  });

  it('Create recipe with error will not redirect', async () => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));

    const wrapper = mount(ModalRecipeCreate);

    vi.spyOn(axios, 'post').mockResolvedValue({
      data: { id: undefined, error: new Error('Unexpected error') }
    });

    const inputs = wrapper.findAll('input');
    await inputs[0].setValue('one');
    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(push).toHaveBeenCalledTimes(0);
  });

  it('Create recipe with loading', async () => {
    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementationOnce(() => ({
      push
    }));

    const wrapper = mount(ModalRecipeCreate);

    vi.spyOn(axios, 'post').mockResolvedValue({
      data: { id: 1, error: undefined }
    });

    const inputs = wrapper.findAll('input');
    await inputs[0].setValue('one');
    await wrapper.find('form').trigger('submit');

    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(wrapper.html()).toContain('Loading ...');

    await flushPromises();

    expect(wrapper.html()).not.toContain('Loading ...');
  });
});
