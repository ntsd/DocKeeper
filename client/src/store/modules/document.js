import api from '../../api'
import {
  GET_DOCUMENT,
  EXTRACT_DOCUMENT,
} from '../types'

const state = {
  document: null
}

const actions = {
  getDocument({ commit }, documentId){
    api.getDocument(documentId).then(response => {
      const json = response.data
      for(var k in json.extracted) { // use to delete _cls in data
        // console.log(k, json.extracted[k]);
        for(const data in json.extracted[k].extractedRules){
          delete json.extracted[k].extractedRules[data]._cls
        }
      }
      // for extract in document.extracted:
      //   for data in extract.extractedRules:
      //           data._cls = None
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
      window.location.reload(true);
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
