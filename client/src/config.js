export const API_ROOT = (process.env.NODE_ENV === 'production')
  ? ''
  : 'http://localhost:8000/'

export const CookieDomain = (process.env.NODE_ENV === 'production')
  ? 'hotcode.me'
  : ''
