import { ParserRuleResource } from './resources'

const addParserRule = (parserId, parserRule) => {
  return ParserRuleResource.save({id:parserId}, parserRule)
}

const getParserRules = (parserId) => {
  return ParserRuleResource.get({id:parserId})
}

const putParserRule = (parserId, parserRule) => {
  return ParserRuleResource.update({id:parserId}, parserRule)
}

export default {
  addParserRule,
  getParserRules,
  putParserRule
}
