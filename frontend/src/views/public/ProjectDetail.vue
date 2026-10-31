<template>
  <div class="project-detail min-h-screen bg-[#050810]">
    <!-- 全局网格背景 -->
    <div class="fixed inset-0 z-0 pointer-events-none bg-grid"></div>

    <!-- 鼠标光斑 (BUG-05 修复) -->
    <div
      ref="glowRef"
      class="fixed w-[500px] h-[500px] rounded-full pointer-events-none z-10 transition-opacity duration-300"
      :style="glowStyle"
    ></div>

    <!-- 返回按钮 -->
    <div class="relative z-20 max-w-4xl mx-auto px-4 md:px-8 pt-8">
      <button
        @click="$router.push('/')"
        class="font-mono text-xs text-text-dim hover:text-neon-green transition-colors"
      >
        ← 返回首页
      </button>
    </div>

    <!-- 主内容 -->
    <div v-if="loading" class="relative z-20 max-w-4xl mx-auto px-4 md:px-8 py-16 text-center">
      <div class="font-mono text-neon-green">加载中...</div>
    </div>

    <div v-else-if="error" class="relative z-20 max-w-4xl mx-auto px-4 md:px-8 py-16 text-center">
      <div class="font-mono text-red-400">{{ error }}</div>
    </div>

    <article v-else class="relative z-20 max-w-4xl mx-auto px-4 md:px-8 py-8 pb-16">
      <!-- 标题 BUG-13 修复：移动端字号调整 -->
      <h1 class="font-rajdhani text-2xl md:text-4xl font-bold text-text-bright mb-4">
        {{ project.title }}
      </h1>

      <!-- 项目简介（未填写时不占位） -->
      <p v-if="project.summary" data-test="project-summary" class="text-text-dim text-base md:text-lg mb-6 leading-relaxed">
        {{ project.summary }}
      </p>

      <!-- 元信息：只显示日期 -->
      <div class="flex items-center font-mono text-xs text-text-dim mb-6">
        <span>{{ formatDate(project.created_at) }}</span>
      </div>

      <!-- 封面图/轮播图 BUG-12 修复：支持多图轮播 -->
      <div
        v-if="hasImages"
        data-test="carousel"
        class="relative h-48 md:h-80 mb-6 bg-gradient-to-br from-bg-panel to-bg-panel-2 border border-line flex items-center justify-center overflow-hidden"
        @mouseenter="isCarouselHovered = true"
        @mouseleave="isCarouselHovered = false"
      >
        <!-- 当前显示的图片 -->
        <img
          :src="currentImage"
          :alt="project.title"
          data-test="carousel-image"
          class="max-h-full max-w-full object-contain transition-opacity duration-300"
        />

        <!-- 多图时显示轮播控制 -->
        <template v-if="allImages.length > 1">
          <!-- 左箭头 -->
          <button
            data-test="carousel-prev"
            @click="prevImage"
            class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/50 hover:bg-black/70 border border-neon-green/30 flex items-center justify-center transition-all"
            style="clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));"
          >
            <span class="text-neon-green text-xl">‹</span>
          </button>

          <!-- 右箭头 -->
          <button
            data-test="carousel-next"
            @click="nextImage"
            class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/50 hover:bg-black/70 border border-neon-green/30 flex items-center justify-center transition-all"
            style="clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));"
          >
            <span class="text-neon-green text-xl">›</span>
          </button>

          <!-- 指示器 -->
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
            <button
              v-for="(img, index) in allImages"
              :key="index"
              @click="goToImage(index)"
              :class="[
                'w-2 h-2 rounded-full transition-all',
                index === currentImageIndex
                  ? 'bg-neon-green w-6'
                  : 'bg-white/30 hover:bg-white/50'
              ]"
            ></button>
          </div>

          <!-- 图片计数 -->
          <div class="absolute top-4 right-4 px-3 py-1 bg-black/50 border border-neon-green/30 font-mono text-xs text-neon-green">
            {{ currentImageIndex + 1 }} / {{ allImages.length }}
          </div>
        </template>
      </div>
      <div
        v-else
        class="h-48 md:h-60 mb-6 bg-gradient-to-br from-bg-panel to-bg-panel-2 border border-line flex items-center justify-center"
      >
        <span class="font-mono text-xs text-text-dim">[ NO IMAGE ]</span>
      </div>

      <!-- 技术栈（未填写时整块隐藏） -->
      <div v-if="techTags.length" data-test="tech-tags" class="flex flex-wrap gap-2 mb-8">
        <span
          v-for="tech in techTags"
          :key="tech"
          class="font-mono text-xs text-neon-green border border-neon-green/30 px-3 py-1"
        >
          {{ tech }}
        </span>
      </div>

      <!-- 正文 -->
      <div
        v-if="renderedContent"
        class="prose prose-invert max-w-none mb-8 markdown-body"
        v-html="renderedContent"
      ></div>
      <div
        v-else
        class="mb-8 border border-line bg-bg-panel px-4 py-8 text-center font-mono text-sm text-text-dim"
      >
        [ 暂无详细介绍 ]
      </div>

      <!-- 外链按钮 BUG-13 修复：移动端响应式 -->
      <div class="flex flex-col md:flex-row gap-3 md:gap-4 mb-8">
        <a
          v-if="project.demo_url"
          :href="project.demo_url"
          target="_blank"
          class="btn-primary font-mono text-sm bg-neon-green text-[#050810] px-6 py-3 font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow inline-block text-center"
          style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
        >
          ▶ 在线演示
        </a>
        <a
          v-if="project.github_url"
          :href="project.github_url"
          target="_blank"
          class="btn-ghost font-mono text-sm text-neon-green border border-neon-green/30 px-6 py-3 hover:bg-neon-green/8 transition-colors inline-block text-center"
          style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
        >
          ◈ GitHub
        </a>
      </div>

      <!-- 页脚信息 BUG-13 修复：移动端响应式 -->
      <div class="pt-6 border-t border-line flex flex-col md:flex-row md:justify-between gap-2 font-mono text-xs text-text-dim">
        <span>浏览量: {{ project.views_count }}</span>
        <span>最后更新: {{ formatDate(project.updated_at) }}</span>
      </div>
    </article>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProjectDetail } from '@/api'
import { getTechTags } from '@/utils/project'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const project = ref(null)
const loading = ref(true)
const error = ref(null)

// BUG-12 修复：图片轮播（支持自动切换）
const currentImageIndex = ref(0)
const isCarouselHovered = ref(false)
const AUTOPLAY_INTERVAL = 4000
let autoplayTimer = null

// BUG-12 修复：合并封面图和项目图片数组
const allImages = computed(() => {
  if (!project.value) return []

  const images = []

  // 如果有项目图片数组，优先使用
  if (project.value.project_images && Array.isArray(project.value.project_images) && project.value.project_images.length > 0) {
    images.push(...project.value.project_images)
  } else if (project.value.cover_image) {
    // 否则使用封面图
    images.push(project.value.cover_image)
  }

  return images
})

// BUG-12 修复：是否有图片
const hasImages = computed(() => allImages.value.length > 0)

// BUG-12 修复：当前显示的图片
const currentImage = computed(() => {
  if (allImages.value.length === 0) return ''
  return allImages.value[currentImageIndex.value]
})

const techTags = computed(() => getTechTags(project.value?.tech_stack))

const stopAutoplay = () => {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

const startAutoplay = () => {
  stopAutoplay()

  // 只有多图时才自动轮播
  if (allImages.value.length <= 1) return

  // 尊重系统“减少动态效果”设置
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return
  }

  autoplayTimer = setInterval(() => {
    // 鼠标悬停或页面不可见时暂停推进
    if (isCarouselHovered.value || document.hidden) return
    currentImageIndex.value = (currentImageIndex.value + 1) % allImages.value.length
  }, AUTOPLAY_INTERVAL)
}

// 指示器点击：切换后重新计时
const goToImage = (index) => {
  currentImageIndex.value = index
  startAutoplay()
}

// 上一张图片
const prevImage = () => {
  if (allImages.value.length <= 1) return
  currentImageIndex.value = (currentImageIndex.value - 1 + allImages.value.length) % allImages.value.length
  startAutoplay()
}

// 下一张图片
const nextImage = () => {
  if (allImages.value.length <= 1) return
  currentImageIndex.value = (currentImageIndex.value + 1) % allImages.value.length
  startAutoplay()
}

// 项目加载或图片列表变化后（重新）启动自动轮播
watch(allImages, (images) => {
  if (currentImageIndex.value >= images.length) {
    currentImageIndex.value = 0
  }
  startAutoplay()
})

// BUG-05 修复：鼠标光斑效果
const glowRef = ref(null)
const mouseX = ref(0)
const mouseY = ref(0)

const glowStyle = computed(() => ({
  left: `${mouseX.value}px`,
  top: `${mouseY.value}px`,
  background: 'radial-gradient(circle, rgba(0,255,200,0.08), transparent 60%)',
  transform: 'translate(-50%, -50%)'
}))

const handleMouseMove = (e) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

// 渲染 Markdown
const renderedContent = computed(() => {
  if (!project.value?.content || !project.value.content.trim()) return ''
  const rawHtml = marked(project.value.content)
  return DOMPurify.sanitize(rawHtml)
})

// 获取项目详情
const fetchProject = async () => {
  try {
    loading.value = true
    project.value = await getProjectDetail(route.params.id)
  } catch (err) {
    error.value = err.detail || '项目不存在'
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

onMounted(() => {
  fetchProject()
  // BUG-05 修复：添加鼠标移动监听
  document.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  // BUG-05 修复：清理鼠标移动监听
  document.removeEventListener('mousemove', handleMouseMove)
  stopAutoplay()
})
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(rgba(0,255,200,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,200,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}
</style>
