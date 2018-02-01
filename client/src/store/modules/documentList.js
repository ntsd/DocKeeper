import api from '../../api'
import {
  GET_DOCUMENT_LIST,
  ADD_DOCUMENT,
  UPDATE_DOCUMENT,
  REQUEST_DOCUMENT_LIST,
  GET_DOCUMENT_LIST_FAILURE, DELETE_DOCUMENT
} from '../types'
import router from '../../router'

const state = {
  items: []
}

const actions = {
  getDocumentListByParser({ commit }, parserId){
    api.getDocumentsByParser(parserId).then(response => {
      const json = response.data
      commit(GET_DOCUMENT_LIST,{
        documentList: json.results
      })
    })
  },
  getDocumentList({ commit }){
    // commit(REQUEST_DOCUMENT_LIST)
    api.getDocumentsByUser().then(response => {
      // console.log('test')
      if(!response.ok){
        return commit(GET_DOCUMENT_LIST_FAILURE)
      }
      const json = response.data
      // const isMore = 0 // !(json.data.length < options.itemsPerPage)
      commit(GET_DOCUMENT_LIST,{
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
  },
  deleteDocument(store, documentId){
    api.deleteDocument(documentId).then(response => {
      store.commit(DELETE_DOCUMENT,{
          documentId: documentId
        })
      // store.getters.deleteDocument(documentId)
    }).catch(e => {
      console.log(e)
    })
  },
  updateDocument(store, [documentId, document]){
    api.putDocument(documentId, document).then(response => {
      store.commit(UPDATE_DOCUMENT,{
        documentId: documentId,
        document: document
      })
      // store.getters.deleteDocument(documentId)
    }).catch(e => {
      console.log(e)
    })
  }
}

const mutations = {
  [GET_DOCUMENT_LIST](state,action){
    state.items = action.documentList
  },
  [ADD_DOCUMENT](state,action){
    state.items.push(action.document)
  },
  [DELETE_DOCUMENT](state, action){
    state.items = state.items.filter(item => item._id.$oid !== action.documentId)
  },
  [UPDATE_DOCUMENT](state, action){
    // const updateIndex = state.items.findIndex((item => item._id.$oid === action.documentId));
    // state.items[updateIndex] = action.document  // this also doesn't work
    const newItems = []
    for (const i in state.items) {
      if (state.items[i]._id.$oid === action.documentId) {
        //state.items[i] = action.document; //i dunno why can't use
        newItems.push(action.document)
      }
      else{
        newItems.push(state.items[i])
      }
    }
    state.items = newItems
  }
}

const getters = {
  // deleteDocument : (state) => (documentId) => {
  //   console.log(state.items[0]._id.$oid, documentId, state.items[0]._id.$oid == documentId)
  //   state.items = state.items.filter(item => item._id.$oid != documentId)
  // }
}

export default {
  state,
  actions,
  mutations,
  getters
}
