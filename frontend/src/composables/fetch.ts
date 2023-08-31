import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import axios from 'axios';
import { ref, type Ref } from 'vue';

interface UseAxiosResult<
  T,
  TExecuteFactory extends (config: AxiosRequestConfig<any>) => Promise<T | undefined>
> {
  result: Ref<T | undefined>;
  isLoading: Ref<boolean>;
  error: Ref<Error | undefined>;
  execute: TExecuteFactory;
}

export function useAxios<T>(
  handleResponse: (response: AxiosResponse<T>) => T
): UseAxiosResult<T, (config: AxiosRequestConfig<any>) => Promise<T | undefined>> {
  const isLoading = ref(false);
  const result = ref<T>();
  const error = ref<Error>();

  const execute = async (config: AxiosRequestConfig<any>) => {
    isLoading.value = true;
    error.value = undefined;
    try {
      const response = await axios.request(config).then(handleResponse);
      result.value = response;
      return response;
    } catch (e) {
      error.value = e as Error;
      result.value = undefined;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    result,
    isLoading,
    error,
    execute
  };
}
