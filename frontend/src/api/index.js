import api from './request'

// ============ 公开接口 ============

// 获取个人信息
export const getProfile = () => api.get('/profile')

// 获取项目列表
export const getProjects = (params) => api.get('/projects', { params })

// 获取重点项目
export const getFeaturedProjects = (limit = 3) => api.get('/projects/featured', { params: { limit } })

// 获取项目详情
export const getProjectDetail = (id) => api.get(`/projects/${id}`)

// ============ 认证接口 ============

// 登录
export const login = (data) => api.post('/auth/login', data)

// ============ 管理接口 ============

// 获取后台项目列表
export const getAdminProjects = () => api.get('/admin/projects')

// 获取项目详情（管理端，不增加浏览量）- BUG-06 修复
export const getAdminProjectDetail = (id) => api.get(`/admin/projects/${id}`)

// 创建项目
export const createProject = (data) => api.post('/admin/projects', data)

// 更新项目
export const updateProject = (id, data) => api.put(`/admin/projects/${id}`, data)

// 删除项目
export const deleteProject = (id) => api.delete(`/admin/projects/${id}`)

// 切换发布状态
export const togglePublish = (id, isPublished) =>
  api.put(`/admin/projects/${id}/publish`, { is_published: isPublished })

// 获取个人信息（管理端）
export const getAdminProfile = () => api.get('/admin/profile')

// 更新个人信息
export const updateProfile = (data) => api.put('/admin/profile', data)

// 上传图片
export const uploadImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/admin/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
