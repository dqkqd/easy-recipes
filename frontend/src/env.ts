const env = import.meta.env;
let _apiUrl = '';
let _fileServerURL = '';

export const defaultImage = '/no-image-icon.png';

if (env.MODE == 'development') {
  _apiUrl = `http://${env.VITE_API_HOST_DEV}`;
  _fileServerURL = `http://${env.VITE_FILE_SERVER_HOST}`;
}

export function convertFileServerDev(url: string | null | undefined) {
  if (!url || env.MODE != 'development') {
    return url;
  }

  const fileServerDevURL = `http://${env.VITE_FILE_SERVER_HOST_DEV}`;

  if (url.startsWith(_fileServerURL)) {
    return url.replace(_fileServerURL, fileServerDevURL);
  }

  if (url.startsWith(fileServerDevURL)) {
    return url.replace(fileServerDevURL, _fileServerURL);
  }

  return url;
}

export const apiUrl = _apiUrl;
