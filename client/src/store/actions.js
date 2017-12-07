import * as types from './types'

export const showMsg = ({commit}, content,type='error') => {
  commit(types.SHOW_MSG, {content:content,type:type})
}

export const hideMsg = ({commit}) => {
  commit(types.HIDE_MSG)
}
