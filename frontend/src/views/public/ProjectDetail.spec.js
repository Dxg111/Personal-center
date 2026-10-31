import { mount, flushPromises } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import ProjectDetail from '@/views/public/ProjectDetail.vue'
import { getProjectDetail } from '@/api'

vi.mock('vue-router', () => ({
  useRoute: () => ({ params: { id: '1' } })
}))

vi.mock('@/api', () => ({
  getProjectDetail: vi.fn()
}))

const baseProject = {
  id: 1,
  title: '测试项目',
  summary: '项目简介',
  content: '# 标题\n\n正文内容',
  cover_image: null,
  project_images: ['/a.jpg', '/b.jpg', '/c.jpg'],
  tech_stack: 'Vue3,FastAPI',
  demo_url: 'https://demo.example.com',
  github_url: 'https://github.com/example/repo',
  category: 'project',
  is_published: true,
  views_count: 12,
  created_at: '2026-10-01T00:00:00',
  updated_at: '2026-10-02T00:00:00'
}

describe('ProjectDetail', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    getProjectDetail.mockResolvedValue({ ...baseProject })
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('渲染 Markdown、技术栈、外链和浏览量', async () => {
    const wrapper = mount(ProjectDetail)
    await flushPromises()

    expect(wrapper.find('h1').text()).toBe('测试项目')
    expect(wrapper.find('.markdown-body').html()).toContain('<h1')
    expect(wrapper.text()).toContain('正文内容')
    expect(wrapper.text()).toContain('Vue3')
    expect(wrapper.text()).toContain('浏览量: 12')
    expect(wrapper.find('a[href="https://demo.example.com"]').exists()).toBe(true)
    expect(wrapper.find('a[href="https://github.com/example/repo"]').exists()).toBe(true)

    wrapper.unmount()
  })

  it('多图轮播自动切换，并在手动切换后重新计时', async () => {
    vi.useFakeTimers()
    const wrapper = mount(ProjectDetail)
    await vi.advanceTimersByTimeAsync(0)
    await nextTick()

    const currentSrc = () => wrapper.find('[data-test="carousel-image"]').attributes('src')
    expect(currentSrc()).toBe('/a.jpg')

    await vi.advanceTimersByTimeAsync(4000)
    await nextTick()
    expect(currentSrc()).toBe('/b.jpg')

    await wrapper.find('[data-test="carousel-next"]').trigger('click')
    await nextTick()
    expect(currentSrc()).toBe('/c.jpg')

    // 手动切换后重新计时，4 秒后从 c 回到 a
    await vi.advanceTimersByTimeAsync(4000)
    await nextTick()
    expect(currentSrc()).toBe('/a.jpg')

    wrapper.unmount()
  })

  it('简介、正文、技术栈为空时显示友好占位', async () => {
    getProjectDetail.mockResolvedValue({
      ...baseProject,
      summary: '',
      content: '',
      tech_stack: '',
      project_images: null,
      cover_image: null
    })

    const wrapper = mount(ProjectDetail)
    await flushPromises()

    expect(wrapper.find('[data-test="project-summary"]').exists()).toBe(false)
    expect(wrapper.find('[data-test="tech-tags"]').exists()).toBe(false)
    expect(wrapper.find('.markdown-body').exists()).toBe(false)
    expect(wrapper.text()).toContain('[ 暂无详细介绍 ]')

    wrapper.unmount()
  })

  it('单图时不显示轮播控制', async () => {
    getProjectDetail.mockResolvedValue({
      ...baseProject,
      project_images: null,
      cover_image: '/only.jpg'
    })

    const wrapper = mount(ProjectDetail)
    await flushPromises()

    expect(wrapper.find('[data-test="carousel-image"]').attributes('src')).toBe('/only.jpg')
    expect(wrapper.find('[data-test="carousel-next"]').exists()).toBe(false)
    expect(wrapper.find('[data-test="carousel-prev"]').exists()).toBe(false)

    wrapper.unmount()
  })
})
