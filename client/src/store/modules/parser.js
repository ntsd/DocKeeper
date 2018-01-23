import api from '../../api'
import {
  GET_PARSER,
  UPDATE_PARSER,
  GET_PARSER_RULE,
  ADD_PARSER_RULE,
  UPDATE_PARSER_RULE
} from '../types'

const state = {
  parser: null,
  parserRules: null,
  parserRule:null
}

const actions = {
  getParser({ commit }, parserId){
    api.getParser(parserId).then(response => {
      const json = response.data
      // console.log("parser" ,json)
      commit(GET_PARSER,{
        parser: json
      })
    })
  },
  addParserRule(store, [parserId, parserRule]){
    // console.log('parserRule',parserId,parserRule)
    api.addParserRule(parserId, parserRule).then(response => {
      const json = response.data
      store.commit(ADD_PARSER_RULE,{
        parser: json
      })
    })
  }
}

const mutations = {
  [GET_PARSER](state,action){
    state.parser = action.parser
  },
  [UPDATE_PARSER](state,action){
    state.parser = action.parser
  },
  [GET_PARSER_RULE](state,action){
    state.parserRule = action.parserRule
  },
  [ADD_PARSER_RULE](state,action){
    state.parser += action.parser
  },
  [UPDATE_PARSER_RULE](state,action){
    state.parser += action.parser
  }
}

export default {
  state,
  actions,
  mutations
}
