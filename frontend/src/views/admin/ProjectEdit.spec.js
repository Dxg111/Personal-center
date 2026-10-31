import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import ProjectEdit from '@/views/admin/ProjectEdit.vue'
import { createProject } from '@/api'

vi.mock('vue-router', () => ({
  useRoute: () => ({ params: {} }),
  useRouter: () => ({ push: vi.fn() })
}))

vi.mock('@/api', () => ({
  getAdminProjectDetail: vi.fn(),
  createProject: vi.fn(),
  updateProject: vi.fn(),
  uploadImage: vi.fn()
}))

describe('ProjectEdit', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('草稿允许空标题，发布前要求填写标题', async () => {
    const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
    const wrapper = mount(ProjectEdit)

    const publishButton = wrapper
      .findAll('button')
      .find((button) => button.text().includes('发 布'))
    expect(publishButton).toBeTruthy()

    await publishButton.trigger('click')
    expect(alertSpy).toHaveBeenCalledWith('发布前请至少填写项目标题')
    expect(createProject).not.toHaveBeenCalled()

    const draftButton = wrapper
      .findAll('button')
      .find((button) => button.text().includes('存草稿'))
    expect(draftButton).toBeTruthy()

    await draftButton.trigger('click')
    await flushPromises()

    expect(createProject).toHaveBeenCalledWith(
      expect.objectContaining({ title: '', is_published: false })
    )

    alertSpy.mockRestore()
    wrapper.unmount()
  })

  it('切换预览模式并清洗危险 HTML', async () => {
    // isVisible 需要组件挂载到 document 上才能正确判断
    const wrapper = mount(ProjectEdit, { attachTo: document.body })
    const preview = () => wrapper.find('[data-test="markdown-preview"]')

    expect(preview().isVisible()).toBe(false)

    await wrapper
      .find('[data-test="content-input"]')
      .setValue('# 标题\n\n<script>alert(1)</script><img src=x onerror=alert(1)>')

    const previewButton = wrapper.findAll('button').find((button) => button.text() === '预览')
    expect(previewButton).toBeTruthy()

    await previewButton.trigger('click')

    expect(preview().isVisible()).toBe(true)
    expect(preview().html()).toContain('<h1')
    expect(preview().text()).toContain('标题')
    expect(preview().html()).not.toContain('<script')
    expect(preview().html()).not.toContain('onerror')

    wrapper.unmount()
  })
})
