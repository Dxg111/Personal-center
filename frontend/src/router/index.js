import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/public/Home.vue')
  },
  {
    path: '/project/:id',
    name: 'ProjectDetail',
    component: () => import('@/views/public/ProjectDetail.vue')
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/admin/Login.vue')
  },
  {
    path: '/admin',
    redirect: '/admin/projects',
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/projects',
    name: 'AdminProjects',
    component: () => import('@/views/admin/ProjectList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/projects/new',
    name: 'AdminProjectNew',
    component: () => import('@/views/admin/ProjectEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/projects/:id/edit',
    name: 'AdminProjectEdit',
    component: () => import('@/views/admin/ProjectEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/profile',
    name: 'AdminProfile',
    component: () => import('@/views/admin/ProfileEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/public/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/admin/login')
  } else if (to.path === '/admin/login' && token) {
    next('/admin/projects')
  } else {
    next()
  }
})

export default router
