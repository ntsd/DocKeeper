import api from '../../api'
import {
  GET_DOCUMENT,
  EXTRACT_DOCUMENT
} from '../types'

const state = {
  document: null
}

const actions = {
  getDocument({ commit }, documentId){
    api.getDocument(documentId).then(response => {
      const json = response.data

      commit(GET_DOCUMENT,{
        document: json
      })
    })
  },
  extractDocument({ commit }, documentId){
    api.extractDocument(documentId).then(response => {
      const json = response.data
      commit(EXTRACT_DOCUMENT, {
        extracted: json
      })
    })
  }
}

const mutations = {
  [GET_DOCUMENT](state,action){
    state.document = action.document
  },
  [EXTRACT_DOCUMENT](state, action){
    state.document.extracted = action.extracted
  }
}

export default {
  state,
  actions,
  mutations
}
