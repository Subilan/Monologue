import Vue from 'vue'
import App from './App.vue'
import store from './store/index';
import './registerServiceWorker'
import router from './router'
import "@/css/mono.less"
import '@mdi/font/css/materialdesignicons.min.css'
import Server from '@/server';
import "vue-material/dist/vue-material.min.css";
import "./css/default.css";
import "./css/override.less";
import "./css/lib.less";
import "./css/mdui.inuse.less";
import NProgress from 'nprogress';
import "./css/nprogress.css";
import "./types";
import mutations from '@/store/mutations';

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
Vue.prototype.$mutations = mutations;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
