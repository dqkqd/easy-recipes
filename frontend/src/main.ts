// import './assets/main.css';

import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import vuetify from '@/plugins/vuetify';
import './assets/main.css';

const app = createApp(App);

app.use(createPinia());
app.use(vuetify);
app.use(router);

app.mount('#app');
