import jwt_decode from 'jwt-decode';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

const env = import.meta.env;
const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
const CURRENT_HREF_KEY = 'CURRENT_HREF_KEY';

const domain = env.VITE_AUTH0_DOMAIN;
const audience = env.VITE_AUTH0_API_AUDIENCE;
const clientId = env.VITE_AUTH0_CLIENT_ID;
const callbackURL = env.VITE_AUTH0_CALLBACK_URL;

function loginLink(callbackPath?: string) {
  let link = 'https://';
  link += domain;
  link += '/authorize?';
  link += 'audience=' + audience + '&';
  link += 'response_type=token&';
  link += 'client_id=' + clientId + '&';
  link += 'redirect_uri=';
  link += callbackPath ? callbackPath : callbackURL;
  return link;
}

export function setJWT(token: string | null) {
  if (token) {
    localStorage.setItem(JWTS_LOCAL_KEY, token);
  }
}

export function removeJWT() {
  localStorage.removeItem(JWTS_LOCAL_KEY);
}

function getJWT() {
  return localStorage.getItem(JWTS_LOCAL_KEY) ?? null;
}

function saveCurrentHref() {
  localStorage.setItem(CURRENT_HREF_KEY, window.location.href);
}

function saveTokenFromHref() {
  const fragment = window.location.hash.slice(1).split('&')[0].split('=');
  if (fragment[0] === 'access_token') {
    const token = fragment[1];
    setJWT(token);
  }
}

function redirectToPreviousHref() {
  saveTokenFromHref();

  const href = localStorage.getItem(CURRENT_HREF_KEY);
  if (href) {
    localStorage.removeItem(CURRENT_HREF_KEY);
    window.location.href = href;
  }
}

export const useAuthStore = defineStore('use-auth-store', () => {
  redirectToPreviousHref();

  const token = ref<string | null>(null);

  const isLoggedIn = computed(() => !!fetchedToken.value);
  const payload = computed(() =>
    fetchedToken.value ? (jwt_decode(fetchedToken.value) as any) : null
  );

  function login() {
    saveCurrentHref();
    window.location.href = loginLink();
  }

  function logout() {
    token.value = null;
    removeJWT();
  }

  function fetchToken() {
    token.value = getJWT();
  }

  const fetchedToken = computed(() => {
    fetchToken();
    return token.value;
  });

  return { isLoggedIn, token: fetchedToken, payload, login, logout };
});
