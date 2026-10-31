import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia } from 'pinia'
import Home from '@/views/public/Home.vue'
import { getProfile, getProjects } from '@/api'

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() })
}))

vi.mock('@/api', () => ({
  getProfile: vi.fn(),
  getProjects: vi.fn()
}))

const makeProject = (id, title, category) => ({
  id,
  title,
  summary: `${title} 的简介`,
  cover_image: null,
  project_images: null,
  tech_stack: 'Vue3,FastAPI',
  category,
  is_published: true,
  views_count: 1,
  created_at: '2026-10-01T00:00:00'
})

const projects = [
  makeProject(1, 'P1', 'project'),
  makeProject(2, 'P2', 'project'),
  makeProject(3, 'P3', 'project'),
  makeProject(4, 'P4', 'project'),
  makeProject(5, 'W1', 'work'),
  makeProject(6, 'W2', 'work')
]

const mountHome = async () => {
  const wrapper = mount(Home, { global: { plugins: [createPinia()] } })
  await flushPromises()
  return wrapper
}

describe('Home', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    getProfile.mockResolvedValue({
      name: 'Tester',
      avatar_url: '/avatar.png',
      bio: '这是简介',
      typing_slogan: '> 文案一\n> 文案二',
      wechat: 'test_wechat',
      email: 'test@example.com',
      github_url: 'https://github.com/tester',
      radar_skills: []
    })
    getProjects.mockResolvedValue(projects.map((project) => ({ ...project })))
  })

  it('展示后台个人信息和首页前三个项目', async () => {
    const wrapper = await mountHome()

    expect(wrapper.text()).toContain('Tester')
    expect(wrapper.text()).toContain('这是简介')

    const avatar = wrapper.find('img[alt="Tester"]')
    expect(avatar.exists()).toBe(true)
    expect(avatar.attributes('src')).toBe('/avatar.png')

    expect(wrapper.findAll('.card')).toHaveLength(3)
    expect(wrapper.text()).toContain('P1')
    expect(wrapper.text()).not.toContain('P4')

    wrapper.unmount()
  })

  it('简介和技术栈为空时显示占位且不生成空标签', async () => {
    getProjects.mockResolvedValue([
      { ...projects[0], title: 'Empty Fields', summary: '', tech_stack: '' }
    ])

    const wrapper = await mountHome()

    expect(wrapper.text()).toContain('暂无简介')
    expect(wrapper.find('.techs').exists()).toBe(false)

    wrapper.unmount()
  })

  it('点击显示更多后展示当前分类的全部项目', async () => {
    const wrapper = await mountHome()

    const moreButton = wrapper.findAll('button').find((button) => button.text().includes('显示更多'))
    expect(moreButton).toBeTruthy()

    await moreButton.trigger('click')
    expect(wrapper.findAll('.card')).toHaveLength(4)
    expect(wrapper.text()).toContain('P4')

    wrapper.unmount()
  })

  it('打字机删除一轮后会继续循环，而不是停在空白', async () => {
    vi.useFakeTimers()

    try {
      const wrapper = mount(Home, { global: { plugins: [createPinia()] } })
      await vi.advanceTimersByTimeAsync(0)

      const typedTexts = []
      for (let i = 0; i < 60; i++) {
        await vi.advanceTimersByTimeAsync(200)
        typedTexts.push(
          wrapper.find('[data-test="typed-slogan"]').text().replace('▊', '')
        )
      }

      // 第一条文案打完并删除后，必须继续显示第二条文案
      expect(typedTexts.some((text) => text.includes('文案一'))).toBe(true)
      expect(typedTexts.some((text) => text.includes('文案二'))).toBe(true)

      wrapper.unmount()
    } finally {
      vi.useRealTimers()
    }
  })

  it('移动端菜单可展开并通过 WORKS 切换分类', async () => {
    const wrapper = await mountHome()

    const toggle = wrapper.find('button[aria-controls="mobile-nav"]')
    expect(toggle.exists()).toBe(true)
    expect(wrapper.find('#mobile-nav').exists()).toBe(false)

    await toggle.trigger('click')
    expect(toggle.attributes('aria-expanded')).toBe('true')
    expect(wrapper.find('#mobile-nav').exists()).toBe(true)

    const worksButton = wrapper
      .findAll('#mobile-nav button')
      .find((button) => button.text().includes('WORKS'))

    await worksButton.trigger('click')

    expect(wrapper.find('#mobile-nav').exists()).toBe(false)
    expect(wrapper.findAll('.card')).toHaveLength(2)
    expect(wrapper.text()).toContain('W1')
    expect(wrapper.text()).not.toContain('P1')

    wrapper.unmount()
  })
})
