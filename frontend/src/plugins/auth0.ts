import { createAuth0 } from '@auth0/auth0-vue';

const env = import.meta.env;

const auth0 = createAuth0({
  domain: env.VITE_AUTH0_DOMAIN,
  clientId: env.VITE_AUTH0_CLIENT_ID,
  authorizationParams: {
    redirect_uri: window.location.origin,
    audience: env.VITE_AUTH0_API_AUDIENCE
  }
});

export default auth0;
