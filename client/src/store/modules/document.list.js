import api from '../../api'
import {
  DOCUMENT_LIST,
  ADD_DOCUMENT_LIST,
  REQUEST_DOCUMENT_LIST,
  GET_DOCUMENT_LIST_FAILURE
} from '../types'
import router from '../../router'

const state = {
  isFetching: false,
  isMore: true,
  items: []
}

const actions = {
  getDocumentList({ commit }, {isAdd=false}){
    commit(REQUEST_DOCUMENT_LIST)
    api.getDocumentsByUser().then(response => {
      // console.log('test')
      if(!response.ok){
        return commit(GET_DOCUMENT_LIST_FAILURE)
      }
      const json = response.data
      const isMore = 0 // !(json.data.length < options.itemsPerPage)
      isAdd
        ? commit(ADD_DOCUMENT_LIST,{
          documentList: json.results,
          isMore:isMore
        })
        : commit(DOCUMENT_LIST,{
          documentList: json.results,
          isMore:isMore
        })
    }, response => {
      commit(GET_DOCUMENT_LIST_FAILURE)
    })
  },
  addDocument({ commit }, document){
    api.addDocument(document).then(response => {
      const json = response.data
      commit(ADD_DOCUMENT_LIST, {'documentList':json})
      router.push({path:'/documents'})
    })
  }
}

const mutations = {
  [REQUEST_DOCUMENT_LIST](state){
    state.isFetching = true
  },
  [DOCUMENT_LIST](state,action){
    state.isFetching = false
    state.isMore = action.isMore
    state.items = action.documentList
  },
  [GET_DOCUMENT_LIST_FAILURE](state){
    state.isFetching = false
  },
  [ADD_DOCUMENT_LIST](state,action){
    state.isFetching = false
    state.isMore = action.isMore
    state.items = [...state.items, ...action.documentList]
  }
}

export default {
  state,
  actions,
  mutations
}
