import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import PasswordEdit from '@/views/admin/PasswordEdit.vue'
import { changePassword } from '@/api'

const push = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => ({ push })
}))

vi.mock('@/api', () => ({
  changePassword: vi.fn()
}))

const mountPage = () => {
  const pinia = createPinia()
  setActivePinia(pinia)
  return mount(PasswordEdit, { global: { plugins: [pinia] } })
}

describe('PasswordEdit', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    changePassword.mockResolvedValue({ message: '密码修改成功' })
  })

  it('两次新密码不一致时拦截提交', async () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
    const wrapper = mountPage()

    await wrapper.find('[data-test="current-password"]').setValue('oldpass123')
    await wrapper.find('[data-test="new-password"]').setValue('newpass123')
    await wrapper.find('[data-test="confirm-password"]').setValue('different123')
    await wrapper.find('form').trigger('submit')

    expect(alertSpy).toHaveBeenCalledWith('两次输入的新密码不一致')
    expect(changePassword).not.toHaveBeenCalled()

    alertSpy.mockRestore()
    wrapper.unmount()
  })

  it('修改成功后清除 Token 并跳转登录页', async () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
    localStorage.setItem('token', 'old-token')

    const wrapper = mountPage()

    await wrapper.find('[data-test="current-password"]').setValue('oldpass123')
    await wrapper.find('[data-test="new-password"]').setValue('newpass123')
    await wrapper.find('[data-test="confirm-password"]').setValue('newpass123')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(changePassword).toHaveBeenCalledWith({
      current_password: 'oldpass123',
      new_password: 'newpass123'
    })
    expect(localStorage.getItem('token')).toBeNull()
    expect(push).toHaveBeenCalledWith('/admin/login')
    expect(alertSpy).toHaveBeenCalledWith('密码修改成功，请使用新密码重新登录')

    alertSpy.mockRestore()
    wrapper.unmount()
  })
})
