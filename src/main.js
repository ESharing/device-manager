import Vue from 'vue'
import { store } from './store'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import './assets/stylesheets/main.css'

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  render: h => h(App)
});

