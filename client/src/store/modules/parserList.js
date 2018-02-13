import api from '../../api'
import {
  GET_PARSER_LIST,
  ADD_PARSER_LIST,
  REQUEST_PARSER_LIST,
  GET_PARSER_LIST_FAILURE,
  SUCCESS_ADD_PARSER,
  DELETE_PARSER, UPDATE_PARSER
} from '../types'
import router from '../../router'

const state = {
  isFetching: false,
  isMore: true,
  items: []
}

const actions = {
  getParserList({ commit }){

    commit(REQUEST_PARSER_LIST)
    api.getParsers().then(response => {
      if(!response.ok){
        return commit(GET_PARSER_LIST_FAILURE)
      }
      const json = response.data
      const isMore = 0 // !(json.data.length < options.itemsPerPage)
      commit(GET_PARSER_LIST,{
        parserList: json.results,
        isMore:isMore
      })
    }, response => {
      commit(GET_PARSER_LIST_FAILURE)
    })
  },
  addParser(store, parser){
    // console.log('add parser', parser)
    api.addParser(parser).then(response => {
      const parser = response.data
      store.commit(SUCCESS_ADD_PARSER,{
        parser: parser
      })
      router.push({path:'/parsers'})
    })
      .catch(e => {
        console.log(e)
      })
  },
  deleteParser(store, parserId){
    // console.log('parserRule',parserId,parserRule)
    api.deleteParser(parserId).then(response => {
      store.commit(DELETE_PARSER,{
        parserId: parserId
      })
    }).catch(
      e => {
        console.log(e)
      }
    )
  },
  updateParser(store, [parserId, parser]){
    api.putParser(parserId, parser).then(response => {
      store.commit(UPDATE_PARSER,{
        parserId: parserId,
        parser:parser
      })
    }).catch(
      e => {
        console.log(e)
      }
    )
  }
}

const mutations = {
  [REQUEST_PARSER_LIST](state){
    state.isFetching = true
  },
  [GET_PARSER_LIST](state,action){
    state.isFetching = false
    state.isMore = action.isMore
    state.items = action.parserList
  },
  [UPDATE_PARSER](state,action){
    const newItems = []
    for (const i in state.items) {
      if (state.items[i]._id.$oid === action.parserId) {
        //state.items[i] = action.document; //i dunno why can't use
        newItems.push(action.parser)
      }
      else{
        newItems.push(state.items[i])
      }
    }
    state.items = newItems
  },
  [DELETE_PARSER](state,action){
    state.items = state.items.filter(item => item._id.$oid !== action.parserId)
  },
  [GET_PARSER_LIST_FAILURE](state){
    state.isFetching = false
  },
  [ADD_PARSER_LIST](state,action){
    state.isFetching = false
    state.isMore = action.isMore || false
    state.items = [...state.items, ...action.parserList]
  },
  [SUCCESS_ADD_PARSER](state,action){
    state.items.push(action.parser)
  }
}

export default {
  state,
  actions,
  mutations
}
