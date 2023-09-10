import { convertFileServerDev, defaultImage } from '@/env';
import type { AxiosRequestConfig, AxiosResponse } from 'axios';
import axios from 'axios';
import { computed, ref, watch, type Ref } from 'vue';

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
  handleResponse: (response: AxiosResponse<T>) => T,
  parseConfigData: (data?: any) => any = (data) => data
): UseAxiosResult<T, (config: AxiosRequestConfig<any>) => Promise<T | undefined>> {
  const isLoading = ref(false);
  const result = ref<T>();
  const error = ref<Error>();

  const execute = async (config: AxiosRequestConfig<any>) => {
    isLoading.value = true;
    error.value = undefined;
    try {
      if (config.data) {
        config.data = parseConfigData(config.data);
      }
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

export function useErrorWithTimeout(error: Ref<Error | undefined>, timeout: number = 3000) {
  const hasError = ref(false);
  watch(error, () => {
    if (error.value) {
      hasError.value = true;
      setTimeout(() => (hasError.value = false), timeout);
    }
  });
  return { hasError };
}

export function useImage(fromSrc: Ref<string>, fromFiles?: Ref<File[]>, initImage?: string | null) {
  const image = convertFileServerDev(initImage);

  const imageSrc = ref(image);

  watch(fromSrc, () => {
    imageSrc.value = fromSrc.value || image;
  });

  if (fromFiles) {
    const reader = new FileReader();
    reader.onload = function () {
      if (reader.result) {
        imageSrc.value = reader.result.toString() || image;
      }
    };

    watch(fromFiles, () => {
      if (fromFiles.value && fromFiles.value.length) {
        reader.readAsDataURL(fromFiles.value[0]);
      } else {
        imageSrc.value = image;
      }
    });
  }

  function onError() {
    imageSrc.value = image;
  }

  const getImage = computed(() => (imageSrc.value === defaultImage ? null : imageSrc.value));
  return { imageSrc, onError, getImage };
}
