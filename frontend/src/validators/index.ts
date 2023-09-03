import { z } from 'zod';

export function validateURL(url: string | null) {
  const trimmedUrl = url ? url.trim() : null;
  const zodURL = z.string().url();
  const { success } = zodURL.safeParse(trimmedUrl);
  return success || 'Invalid URL';
}

export function required(label: string) {
  function inner(field: string | null) {
    return !!field || `${label} is required`;
  }
  return inner;
}
