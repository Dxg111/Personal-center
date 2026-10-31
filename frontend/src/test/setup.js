import { vi } from 'vitest'

// jsdom 未实现 matchMedia，轮播自动播放会读取 prefers-reduced-motion
if (!window.matchMedia) {
  window.matchMedia = vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
}

// jsdom 未实现 scrollTo / scrollIntoView
window.scrollTo = vi.fn()

if (!Element.prototype.scrollIntoView) {
  Element.prototype.scrollIntoView = vi.fn()
}
