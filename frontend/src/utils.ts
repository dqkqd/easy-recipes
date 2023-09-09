export const supportedImages = ['image/png', 'image/jpg', 'image/jpeg'];

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
