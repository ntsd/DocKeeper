import { ParserResource } from './resources'

const addParser = (parser) => {
  return ParserResource.save({id:'add'},parser)
}

const getParser = (parserId) => {
  return ParserResource.get({id:parserId})
}

const putParser = (parserId, parser) => {
  return ParserResource.update({id:parserId}, parser)
}

const deleteParser = (parserId) => {
  return ParserResource.delete({id:parserId})
}

const getParsers = () => {
  return ParserResource.get({id:'list'})
}

export default {
  addParser,
  getParser,
  getParsers,
  putParser,
  deleteParser
}
