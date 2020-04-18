import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import "@/css/mono.less"
import '@mdi/font/css/materialdesignicons.min.css'
import Server from '@/server';
import "vue-material/dist/vue-material.min.css";
import "./css/default.css";
import "./css/override.less";

Vue.config.productionTip = false
Vue.prototype.$server = Server;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
