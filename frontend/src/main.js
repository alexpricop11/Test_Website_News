import {createApp} from 'vue';
import App from './App.vue';
import router from './router/routing.js';
import '@fortawesome/fontawesome-free/css/all.css';

const app = createApp(App);

app.use(router);
app.mount('#app');

