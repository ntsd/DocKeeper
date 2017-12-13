import api from '../../api'
import {
  GET_PARSER
} from '../types'

const state = {
  parser: null,
  parserRules: null
}

const actions = {
  getParser({ commit }, parserId){
    api.getParser(parserId).then(response => {
      const json = response.data
      // console.log("parser",json)
      commit(GET_PARSER,{
        parser: json
      })
    })
  }
}

const mutations = {
  [GET_PARSER](state,action){
    state.parser = action.parser
  }
}

export default {
  state,
  actions,
  mutations
}
