import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import axios from 'axios';
import { ref, toValue, watchEffect, type Ref } from 'vue';

export function useFetch(url: string) {
  const data = ref();
  const error = ref<Error>();

  watchEffect(async () => {
    data.value = null;
    error.value = undefined;
    const urlValue = toValue(url);

    try {
      const res = await fetch(urlValue);
      data.value = await res.json();
    } catch (e) {
      error.value = e as Error;
    }
  });

  return { data, error };
}

export function useFetchWithParsable<Type>(
  c: { parse(data: unknown): Type },
  url: string
): { data: Ref<Type>; error: Ref<Error | undefined> } {
  const data = ref();
  const error = ref<Error>();

  watchEffect(async () => {
    data.value = null;
    error.value = undefined;
    const urlValue = toValue(url);

    try {
      const res = await fetch(urlValue);
      const jsonData = await res.json();
      data.value = c.parse(jsonData);
    } catch (e) {
      error.value = e as Error;
    }
  });

  return { data, error };
}

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
      const response = await axios(config).then(handleResponse);
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
