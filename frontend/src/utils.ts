export const supportedImages = ['image/png', 'image/jpg', 'image/jpeg'];
export const RECIPE_INGREDIENT_PER_PAGE = 9;
export const INGREDIENT_RECIPE_PER_PAGE = 9;
export function replaceBase64Prefix(base64Img: string | null) {
  for (const supportedImage of supportedImages) {
    const base64ImagePrefix = `data:${supportedImage};base64,`;
    if (base64Img && base64Img.startsWith(base64ImagePrefix)) {
      base64Img = base64Img.replace(base64ImagePrefix, '');
      break;
    }
  }
  return base64Img;
}

export function stripText(text: string, length: number) {
  return text.length <= length ? text : text.slice(0, length - 1) + '…';
}
