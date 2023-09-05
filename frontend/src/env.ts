const env = import.meta.env;
let _apiUrl = '';
let _fileServerURL = '';

const defaultImage = '/no-image-icon.png';

if (env.MODE == 'development') {
  _apiUrl = `http://${env.VITE_API_HOST_DEV}`;
  _fileServerURL = `http://${env.VITE_FILE_SERVER_HOST}`;
}

export function convertFileServerDev(url: string | null | undefined) {
  if (!url) {
    return defaultImage;
  }

  if (env.MODE != 'development') {
    return url;
  }
  if (!url.startsWith(_fileServerURL)) {
    return url;
  }

  const fileServerDevURL = `http://${env.VITE_FILE_SERVER_HOST_DEV}`;
  return url.replace(_fileServerURL, fileServerDevURL);
}

export const apiUrl = _apiUrl;
