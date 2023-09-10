const env = import.meta.env;
let _apiUrl = '';
let _fileServerURL = '';

export const defaultImage = '/no-image-icon.png';

if (env.MODE == 'development') {
  _apiUrl = `http://${env.VITE_API_HOST_DEV}`;
  _fileServerURL = `http://${env.VITE_FILE_SERVER_HOST}`;
}

const fileServerDevURL = `http://${env.VITE_FILE_SERVER_HOST_DEV}`;

export function urlToDev(url: string | null) {
  if (!url || env.MODE !== 'development') {
    return url;
  }
  return url.replace(_fileServerURL, fileServerDevURL);
}

export function urlFromDev(url: string | null) {
  if (!url || env.MODE !== 'development') {
    return url;
  }
  return url.replace(fileServerDevURL, _fileServerURL);
}

export const apiUrl = _apiUrl;
