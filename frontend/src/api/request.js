import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：自动添加 Token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      // 401 未授权，跳转登录
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/admin/login'
      }
      return Promise.reject(error.response.data)
    }
    return Promise.reject(error)
  }
)

export default api
