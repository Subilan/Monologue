import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import "@/css/mono.less"
import '@mdi/font/css/materialdesignicons.min.css'
import Server from '@/server';

Vue.config.productionTip = false
Vue.prototype.$server = Server;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
