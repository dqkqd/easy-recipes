import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import vuetify from '@/plugins/vuetify';
import { createAuth0 } from '@auth0/auth0-vue';
import './assets/main.css';

const app = createApp(App);

const env = import.meta.env;

app.use(createPinia());
app.use(
  createAuth0({
    domain: env.VITE_AUTH0_DOMAIN,
    clientId: env.VITE_AUTH0_CLIENT_ID,
    authorizationParams: {
      redirect_uri: window.location.origin,
      audience: env.VITE_AUTH0_API_AUDIENCE
    }
  })
);
app.use(vuetify);
app.use(router);

app.mount('#app');
