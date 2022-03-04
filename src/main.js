import Vue from 'vue'
import { store } from './store'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router';

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  render: h => h(App)
});

