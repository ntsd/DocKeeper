import api from '../../api'
import {showMsg} from '../actions'
import {
  LOGIN_SUCCESS,
  USERINFO_SUCCESS,
  USERINFO_FAILURE,
  LOGOUT_USER,
  UPDATE_USER_SUCCESS
} from '../types'
import { getCookie,saveCookie,signOut } from '../../utils/authService'
import router from '../../router'

const state = {
  token: getCookie('token') || null,
  user: null
}

const actions = {
  logout({commit}){
    signOut()
    commit(LOGOUT_USER)
    // window.location.pathname = '/'
    router.push({path:'/pages/login'})
  },
  localLogin(store, userInfo){
    api.login(userInfo).then(response => {
      if(!response.ok){
        return showMsg(store,response.data.error_msg || 'url  wrong')
      }
      const token = response.data.access_token
      saveCookie('token',token)
      //store.dispatch('getUserInfo') // store user info no need to get in vue component
      store.commit(LOGIN_SUCCESS, {token: token })
      showMsg(store,'login success','success')
      router.push({path:'/'})
    }, response => {
      showMsg(store,response.data.error_msg || 'can\'t login')
    })
  },
  getUserInfo({ commit }){
    api.getMe().then(response => {
      if(!response.ok){
        return commit(USERINFO_FAILURE)
      }
      commit(USERINFO_SUCCESS, { user: response.data })
    }, response => {
      commit(USERINFO_FAILURE)
    })
  },
  updateUser(store,userInfo){
    api.mdUser(userInfo).then(response => {
      if(!response.ok){
        return showMsg(store,'更新用户资料失败!')
      }
      store.commit(UPDATE_USER_SUCCESS, { user: response.data.data })
      showMsg(store,'更新资料成功!','success')
    }, response => {
      showMsg(store,'更新用户资料失败!')
    })
  }
}



const mutations = {
  [LOGIN_SUCCESS](state , action){
    state.token = action.token
  },
  [USERINFO_SUCCESS](state,action){
    state.user = action.user
  },
  [USERINFO_FAILURE](state,action){
    state.user = null
  },
  [LOGOUT_USER](state,action){
    state.token = getCookie('token') || null
    state.user = null
    //state.token = null
  },
  [UPDATE_USER_SUCCESS](state,action){
    state.user = action.user
  }
}

export default {
  state,
  actions,
  mutations
}
