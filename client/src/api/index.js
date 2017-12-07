// import user from './user'
// import parser from './parser'
// import parserRule from './parserRule'
// import document from './document'
import {UserResource, ParserResource, ParserRuleResource, DocumentResource} from './resources'

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
  // Document
  getDocument : (id) => {
    return DocumentResource.get({id:id})
  },

  putDocument : (id, document) => {
    return DocumentResource.update({id:id},document)
  },

  deleteDocument : (id) => {
    return DocumentResource.delete({id:id})
  },

  addDocument : (document) => {
    return this.$http.post('/documents/add', document, {
      emulateJSON: true,
      headers: {
        'X-File-Name': 'my_image',
// 'Content-Type': 'multipart/form-data'
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
      ) // DocumentResource.save({id:'add'}, document)
  },

  getDocuments : (parserId) => {
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
