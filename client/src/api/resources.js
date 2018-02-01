import Vue from 'vue'
import VueResource from 'vue-resource'
import {API_ROOT} from '../config'
import { getCookie,signOut,isLogin } from '../utils/authService'

Vue.use(VueResource)

Vue.http.options.crossOrigin = false//true it will has options
Vue.http.options.credentials = false

Vue.http.interceptors.push((request, next)=>{
  request.headers = request.headers || {}
  if (isLogin()) {
    request.headers.set('Authorization', 'Bearer '+ getCookie('token').replace(/(^\")|(\"$)/g, ''))
  }
  next((response) => {
    if (response.status === 401) {
      signOut()
      window.location.pathname = '/login'
    }
  })
})

export const http = Vue.http
export const UserResource = Vue.resource(API_ROOT + 'users{/id}')
export const ParserResource = Vue.resource(API_ROOT + 'parsers{/id}')
export const ParserRuleResource = Vue.resource(API_ROOT + 'parserrules{/id}')
export const DocumentResource = Vue.resource(API_ROOT + 'documents{/id}')
