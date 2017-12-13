import api from '../../api'
import {
  DOCUMENT_LIST,
  ADD_DOCUMENT,
  REQUEST_DOCUMENT_LIST,
  GET_DOCUMENT_LIST_FAILURE
} from '../types'
import router from '../../router'

const state = {
  items: []
}

const actions = {
  getDocumentListByParser({ commit }, parserId){
    api.getDocumentsByParser(parserId).then(response => {
      const json = response.data
      commit(DOCUMENT_LIST,{
        documentList: json.results
      })
    })
  },
  getDocumentList({ commit }){
    commit(REQUEST_DOCUMENT_LIST)
    api.getDocumentsByUser().then(response => {
      // console.log('test')
      if(!response.ok){
        return commit(GET_DOCUMENT_LIST_FAILURE)
      }
      const json = response.data
      // const isMore = 0 // !(json.data.length < options.itemsPerPage)
      commit(DOCUMENT_LIST,{
        documentList: json.results
      })
      // isAdd
      //   ? commit(ADD_DOCUMENT_LIST,{
      //     documentList: json.results
      //   })
      //   : commit(DOCUMENT_LIST,{
      //     documentList: json.results
      //   })
    }, response => {
      commit(GET_DOCUMENT_LIST_FAILURE)
    })
  },
  addDocument(store, form){
    const document = {name:form.name,
      parserRef:{
        id:form.parserRef._id,
        name:form.parserRef.name
      }
    };
    // console.log(document)
    api.addDocument(document).then(response => {
      const document = response.data
      api.uploadDocument(document._id.$oid, form.parserRef._id.$oid, form.file).then(response => {
        // console.log(response.data)
        document.path = response.data
      })
      // console.log(document)
      // store.commit(ADD_DOCUMENT,{
      //   document: document
      // }) // to do
      router.push({path:'/documents'})
    }).catch(e => {
      console.log(e)
    })
  }
}

const mutations = {
  [DOCUMENT_LIST](state,action){
    state.items = action.documentList
  },
  [ADD_DOCUMENT](state,action){
    state.items.push(action.document)
  }
}

export default {
  state,
  actions,
  mutations
}
