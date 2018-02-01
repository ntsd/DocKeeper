import Vue from 'vue'
import Router from 'vue-router'

// Containers
import Full from '@/containers/Full'

// Views
import Dashboard from '@/views/Dashboard'
import Parsers from '@/views/parsers/Parsers'
import Parser from '@/views/parsers/Parser'
import ParserRule from '@/views/parsers/ParserRule'
import NewParser from '@/views/parsers/NewParser'
import Documents from '@/views/documents/Documents'
import Document from '@/views/documents/Document'
import UploadDocument from '@/views/documents/UploadDocument'

// Views - Pages
import Page404 from '@/views/pages/Page404'
import Page500 from '@/views/pages/Page500'
import Login from '@/views/pages/Login'
import Register from '@/views/pages/Register'

import {isLogin} from '../utils/authService'

Vue.use(Router)

const router = new Router({
  mode: 'hash', // Demo is living in GitHub.io, so required!
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/parsers',//'/dashboard',
      name: 'Home',
      component: Full,
      meta: {
        requiresAuth: true
      },
      children: [
        // {
        //   path: 'dashboard',
        //   name: 'Dashboard',
        //   component: Dashboard
        // },
        {
          path: 'parsers',
          name: 'Parsers',
          component: Parsers
        },
        {
          path: 'newparser',
          name: 'New Parser',
          component: NewParser
        },
        {
          path: 'documents',
          name: 'Documents',
          component: Documents
        },
        {
          path: 'uploaddocument/:parserId',
          name: 'Upload Document',
          component: UploadDocument
        },
        {
          path: 'parser/:parserId',
          name: Parser.name,
          component: Parser
        },
        {
          path: 'document/:documentId',
          name: 'Document',
          component: Document
        },
        {
          path: 'parser/:parserId/:parserRuleId',
          name: 'Parser Rule',
          component: ParserRule
        }
      ]
    },
    {
      path: '/pages',
      redirect: '/pages/p404',
      name: 'Pages',
      component: {
        render (c) { return c('router-view') }
      },
      children: [
        {
          path: '404',
          name: 'Page404',
          component: Page404
        },
        {
          path: '500',
          name: 'Page500',
          component: Page500
        },
        {
          path: 'login',
          name: 'Login',
          component: Login
        },
        {
          path: 'register',
          name: 'Register',
          component: Register
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.goTop)) {
    window.scroll(0, 0)
  }

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLogin()) {
      return next({path: '/pages/login'})
    }
  }
  if (to.matched.some(record => record.meta.requiresNotAuth)) {
    if (isLogin()) {
      return next({path: '/'})
    }
  }
  next()
})

export default router
