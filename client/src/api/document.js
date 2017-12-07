import { DocumentResource } from './resources'

const getDocument = (id) => {
  return DocumentResource.get({id:id})
}

const putDocument = (id, document) => {
  return DocumentResource.update({id:id},document)
}

const deleteDocument = (id) => {
  return DocumentResource.delete({id:id})
}

const addDocument = (document) => {
  return DocumentResource.save({id:'add'}, document)
}

const getDocuments = (parserId) => {
  return DocumentResource.get({id:'list/'+parserId})
}

export default {
  getDocument,
  putDocument,
  deleteDocument,
  addDocument,
  getDocuments
}
