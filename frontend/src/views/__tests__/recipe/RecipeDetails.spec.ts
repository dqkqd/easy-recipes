import { describe, expect, it, vi } from 'vitest';

import { apiUrl } from '@/env';
import { RecipeSchema } from '@/schema/recipe';
import RecipeDetails from '@/views/recipe/RecipeDetails.vue';
import { flushPromises, mount } from '@vue/test-utils';
import axios from 'axios';
import { useRouter } from 'vue-router';

describe('RecipeDetails', () => {
  const recipe = RecipeSchema.parse({
    id: 1,
    name: 'Recipe name',
    description: 'Recipe description',
    image_uri: 'http://localhost:8080/valid-image-url',
    ingredients: []
  });

  describe('Render properly', () => {
    it('Render recipe successfully', async () => {
      vi.spyOn(axios, 'request').mockResolvedValue({
        data: recipe
      });

      const wrapper = mount(RecipeDetails, { props: { id: 1 } });
      await flushPromises();

      expect(axios.request).toBeCalledTimes(1);
      expect(axios.request).toBeCalledWith({
        method: 'get',
        url: `${apiUrl}/recipes/${recipe.id}`
      });

      expect(wrapper.find('[data-test=recipe-details-name]').text()).toBe(recipe.name);
      expect(wrapper.find('[data-test=recipe-details-description]').text()).toBe(
        recipe.description
      );
      expect(wrapper.find('[data-test=recipe-details-valid-image]').attributes('src')).toBe(
        recipe.image_uri
      );

      expect(wrapper.find('[data-test=recipe-details-error]').exists()).toBe(false);
      expect(wrapper.find('[data-test=recipe-details-loading]').exists()).toBe(false);
      expect(wrapper.find('[data-test=recipe-details-default-image]').exists()).toBe(false);
      expect(wrapper.find('[data-test=delete-button]').exists()).toBe(true);
    });

    it('Render default image successfully', async () => {
      const recipeWithNullImage = recipe;
      recipeWithNullImage.image_uri = null;

      vi.spyOn(axios, 'request').mockResolvedValue({
        data: recipeWithNullImage
      });

      const wrapper = mount(RecipeDetails, { props: { id: 1 } });
      await flushPromises();

      expect(axios.request).toBeCalledTimes(1);
      expect(axios.request).toBeCalledWith({
        method: 'get',
        url: `${apiUrl}/recipes/${recipeWithNullImage.id}`
      });

      expect(wrapper.find('[data-test=recipe-details-name]').text()).toBe(recipeWithNullImage.name);
      expect(wrapper.find('[data-test=recipe-details-description]').text()).toBe(
        recipeWithNullImage.description
      );
      expect(wrapper.find('[data-test=recipe-details-default-image]').attributes('src')).toBe(
        '/no-image-icon.png'
      );
    });

    it('Render with loading', async () => {
      vi.spyOn(axios, 'request').mockResolvedValue({
        data: recipe
      });

      const wrapper = mount(RecipeDetails, { props: { id: 1 } });

      expect(wrapper.find('[data-test=recipe-details-loading]').text()).toBe('Loading ...');
    });

    it('Render with error', async () => {
      vi.spyOn(axios, 'request').mockImplementation(() => {
        throw new Error('Unexpected error');
      });

      const wrapper = mount(RecipeDetails, { props: { id: 1 } });
      await flushPromises();

      expect(axios.request).toBeCalledTimes(1);
      expect(axios.request).toBeCalledWith({
        method: 'get',
        url: `${apiUrl}/recipes/1`
      });
      expect(wrapper.find('[data-test=recipe-details-error]').text()).toBe('Something wrong ...');
    });
  });

  describe('Delete Recipe', () => {
    vi.mock('vue-router', () => ({
      useRouter: vi.fn(() => ({
        push: () => {}
      }))
    }));

    const push = vi.fn();
    // @ts-ignore
    useRouter.mockImplementation(() => ({
      push
    }));

    it('Delete successfully', async () => {
      vi.spyOn(axios, 'request').mockResolvedValueOnce({
        data: recipe
      });

      const wrapper = mount(RecipeDetails, { props: { id: 1 } });
      await flushPromises();

      vi.spyOn(axios, 'request').mockResolvedValueOnce({
        data: { id: 1 }
      });

      await wrapper.find('[data-test=delete-button]').trigger('click');

      expect(wrapper.find('[data-test=recipe-details-delete-loading]').exists()).toBe(true);
      expect(wrapper.find('[data-test=recipe-details-delete-loading]').text()).toBe('Deleting ...');

      await flushPromises();

      expect(axios.request).toBeCalledTimes(1);
      expect(axios.request).toBeCalledWith({
        method: 'delete',
        url: `${apiUrl}/recipes/${recipe.id}`,
        headers: {
          authorization: 'bearer delete:recipe'
        }
      });

      expect(push).toHaveBeenCalledTimes(1);
      expect(push).toBeCalledWith({ name: 'home' });

      expect(wrapper.find('[data-test=recipe-details-delete-error]').exists()).toBe(false);
      expect(wrapper.find('[data-test=recipe-details-delete-loading]').exists()).toBe(false);
    });

    it('Delete with error', async () => {
      vi.spyOn(axios, 'request').mockResolvedValueOnce({
        data: recipe
      });

      const wrapper = mount(RecipeDetails, { props: { id: 1 } });
      await flushPromises();

      vi.spyOn(axios, 'request').mockImplementationOnce(() => {
        throw new Error('Unexpected error');
      });

      await wrapper.find('[data-test=delete-button]').trigger('click');
      await flushPromises();

      expect(wrapper.find('[data-test=recipe-details-delete-error]').text()).toBe(
        'Error while deleting ...'
      );
    });
  });
});
