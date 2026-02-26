import './assets/main.css'
import Vue from 'vue';
import FlashMessage from '@smartweb/vue-flash-message';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import "bootswatch/dist/quartz/bootstrap.min.css";
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
Vue.use(FlashMessage);

app.mount('#app')
