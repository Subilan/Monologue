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
import "./css/lib.less";
import NProgress from 'nprogress';
import "./css/nprogress.css";

NProgress.configure({
  showSpinner: false,
})

router.beforeEach((to, from, next) => {
  NProgress.start();
  next();
})

router.afterEach(t => {
  NProgress.done();
})

Vue.config.productionTip = false
Vue.prototype.$server = Server;

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
