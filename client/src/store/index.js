import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'
import * as actions from './actions'
import * as getters from './getters'
import parserList from './modules/parserList'
import documentList from './modules/documentList'
import parser from './modules/parser'
import document from './modules/document'
import auth from './modules/auth'
import showmsg from './modules/showmsg'

const debug = process.env.NODE_ENV !== 'production'
Vue.use(Vuex)

export default new Vuex.Store({
  actions,
  getters,
  modules: {
    auth,
    parserList,
    documentList,
    parser,
    document,
    showmsg,
  },
  strict: true,
  // strict: debug,
  plugins: debug ? [createLogger()] : []
})
