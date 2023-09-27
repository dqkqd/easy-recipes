const env = import.meta.env;
const _apiUrl = env.VITE_API_HOST;

const fileServerHost = env.VITE_FILE_SERVER_HOST;
const fileServerHostDev = env.VITE_FILE_SERVER_HOST_DEV;

const shouldConvertURL = env.VITE_FORCE_CONVERT_URL === 'true' || env.MODE === 'development';

export const defaultImage = '/no-image-icon.png';

export function urlToDev(url: string | null) {
  if (!url || !shouldConvertURL) {
    return url;
  }

  return url.replace(fileServerHost, fileServerHostDev);
}

export function urlFromDev(url: string | null) {
  if (!url || !shouldConvertURL) {
    return url;
  }
  return url.replace(fileServerHostDev, fileServerHost);
}

export const apiUrl = _apiUrl;
