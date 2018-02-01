// import user from './user'
// import parser from './parser'
// import parserRule from './parserRule'
// import document from './document'
import {UserResource, ParserResource, ParserRuleResource, DocumentResource, http} from './resources'

export default {
  // User
  login : (credentials) => {
    return UserResource.save({id:'login'},credentials)
  },

  register : (user) => {
    return UserResource.save({id:'register'},user)
  },

  getMe : () => {
    return UserResource.get({id:'me'})
  },
  // Parser
  addParser : (parser) => {
    return ParserResource.save({id:'add'},parser)
  },

  getParser : (parserId) => {
    return ParserResource.get({id:parserId})
  },

  putParser : (parserId, parser) => {
    return ParserResource.update({id:parserId}, parser)
  },

  deleteParser : (parserId) => {
    return ParserResource.delete({id:parserId})
  },

  getParsers : () => {
    return ParserResource.get({id:'list'})
  },
  // ParserRule
  addParserRule : (parserId, parserRule) => {
    return ParserRuleResource.save({id:parserId}, parserRule)
  },

  getParserRules : (parserId) => {
    return ParserRuleResource.get({id:parserId})
  },

  putParserRule : (parserId, parserRule) => {
    return ParserRuleResource.update({id:parserId}, parserRule)
  },
  deleteParserRule : (parserId, parserRule) => {
    return ParserRuleResource.delete({id:parserId}, parserRule)
  },
  // Document
  getDocument : (documentId) => {
    return DocumentResource.get({id:documentId})
  },

  putDocument : (documentId, document) => {
    return DocumentResource.update({id:documentId},document)
  },

  deleteDocument : (documentId) => {
    return DocumentResource.delete({id:documentId})
  },

  addDocument : (document) => {
    return DocumentResource.save({id:'add'}, document)
  },

  uploadDocument : (documentId, parserId, documentFile) => {
    var formData = new FormData();
    formData.append('document-file', documentFile);
    formData.append('parserId', parserId);
    return http.post('http://127.0.0.1:8000/documents/upload/'+documentId, formData, {
          emulateJSON: true,
          headers: {
            // 'X-File-Name': 'my_image',
            'Content-Type': 'multipart/form-data'
          }}
    )
  },

  extractDocument : (documentId) => {
    // console.log('extract', documentId)
    return DocumentResource.get({id:'extract/'+documentId})
  },

  getDocumentsByParser : (parserId) => {
    return DocumentResource.get({id:'list/'+parserId})
  },

  getDocumentsByUser : () => {
    return DocumentResource.get({id:'list'})
  },

  // user,
  // parser,
  // parserRule,
  // document,
}
