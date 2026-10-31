import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from './auth'

describe('auth store', () => {
  beforeEach(() => {
    localStorage.clear()
    setActivePinia(createPinia())
  })

  it('保存和清除 Token', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)

    store.setToken('test-token')
    expect(store.token).toBe('test-token')
    expect(store.isAuthenticated).toBe(true)
    expect(localStorage.getItem('token')).toBe('test-token')

    store.clearToken()
    expect(store.token).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('token')).toBeNull()
  })
})
