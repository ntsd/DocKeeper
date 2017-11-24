import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

// Containers
import Full from '@/containers/Full'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/app',
      name: 'App',
      component: Full
    }

  ]
})
