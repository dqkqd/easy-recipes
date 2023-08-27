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
