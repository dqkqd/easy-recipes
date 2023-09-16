import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import auth0 from '@/plugins/auth0';
import vuetify from '@/plugins/vuetify';
import './assets/main.css';

const app = createApp(App);

app.use(createPinia());
app.use(auth0);
app.use(vuetify);
app.use(router);

app.mount('#app');
