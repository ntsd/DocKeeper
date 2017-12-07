// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import { sync } from 'vuex-router-sync'
import store from './store'
import router from './router'
import moment from 'moment'

Vue.use(BootstrapVue)

Vue.prototype.moment = moment

sync(store, router)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {
    App
  }
})
