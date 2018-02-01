import api from '../../api'
import {
  GET_PARSER,
  UPDATE_PARSER, //Parser Rule
  GET_PARSER_RULE,
  ADD_PARSER_RULE,
  UPDATE_PARSER_RULE,
  DELETE_PARSER_RULE
} from '../types'
import router from '../../router'

const state = {
  parser: null,
  parserRules: null,
  parserRule:null
}

const actions = {
  //parser
  getParser({ commit }, parserId){
    api.getParser(parserId).then(response => {
      const json = response.data
      // console.log("parser" ,json)
      commit(GET_PARSER,{
        parser: json
      })
    })
  },
  //parser Rule
  addParserRule(store, [parserId, parserRule]){ // todo do not refresh at first time
    // console.log('parserRule',parserId,parserRule)
    api.addParserRule(parserId, parserRule).then(response => {
      const json = response.data
      store.commit(ADD_PARSER_RULE,{
        parser: json
      })
      // console.log(parserId)
      router.push({path: '/parser/'+parserId})
    }).catch(
      e => {
        console.log(e)
      }
    )
  },
  deleteParserRule(store, [parserId, parserRule]){
    api.deleteParserRule(parserId, parserRule).then(response => {
      store.commit(DELETE_PARSER_RULE,{
        parserRuleId: parserRule.oid.$oid
      })
      router.push({path: '/parser/'+parserId})
    }).catch(
      e => {
        console.log(e)
      }
    )
  },
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
  },
  [DELETE_PARSER_RULE](state,action){
    state.parser.parserRules = state.parser.parserRules.filter(item => item.oid.$oid !== action.parserRuleId)
  }
}

export default {
  state,
  actions,
  mutations
}
