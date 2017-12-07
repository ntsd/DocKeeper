import { UserResource } from './resources'
import { API_ROOT } from '@/config'

const login = (credentials) => {
  return UserResource.save({id:'login'},credentials)
}

const register = (user) => {
  return UserResource.save({id:'register'},user)
}

export default {
  login,
  register
}
