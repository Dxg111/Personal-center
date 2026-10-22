<template>
  <div class="home">
    <!-- 全局网格背景 -->
    <div class="fixed inset-0 z-0 pointer-events-none bg-grid"></div>

    <!-- 鼠标光斑 -->
    <div
      ref="glowRef"
      class="fixed w-[500px] h-[500px] rounded-full pointer-events-none z-10 transition-opacity duration-300"
      :style="glowStyle"
    ></div>

    <!-- 顶部状态条 BUG-13 修复：移动端适配 -->
    <div class="topbar relative z-20 flex justify-between items-center px-4 md:px-12 py-4 border-b border-line font-mono text-xs text-text-dim">
      <div class="brand text-text-bright font-medium tracking-wider text-xs md:text-sm">
        RED岸 <span class="text-neon-green">// STATION</span>
      </div>
      <div class="nav hidden md:flex gap-6">
        <a href="#" class="hover:text-neon-green transition-colors">HOME</a>
        <a href="#projects" @click.prevent="scrollToProjects('project')" class="hover:text-neon-green transition-colors">PROJECTS</a>
        <a href="#projects" @click.prevent="scrollToProjects('work')" class="hover:text-neon-green transition-colors">WORKS</a>
        <a href="#contact" class="hover:text-neon-green transition-colors">CONTACT</a>
      </div>
      <div class="hidden md:block">
        <span class="inline-block w-2 h-2 rounded-full bg-neon-green shadow-[0_0_8px_#00ffc8] animate-blink mr-2"></span>
        ONLINE · UTC+8
      </div>
      <div class="md:hidden">
        <span class="inline-block w-2 h-2 rounded-full bg-neon-green shadow-[0_0_8px_#00ffc8] animate-blink"></span>
      </div>
    </div>

    <!-- Hero 区 BUG-13 修复：移动端适配 -->
    <section class="hero relative z-20 max-w-7xl mx-auto px-4 md:px-12 py-10 md:py-20 grid md:grid-cols-2 gap-10 items-center min-h-[50vh] md:min-h-[70vh]">
      <!-- 左侧内容 -->
      <div class="hero-left">
        <div class="font-mono text-xs text-neon-green mb-3 md:mb-5">~/home — 欢迎访问我的信号站</div>
        <h1 class="font-rajdhani text-3xl md:text-5xl font-bold text-text-bright leading-tight tracking-wide">
          你好，我是<em class="text-neon-green not-italic">{{ profile?.name || 'Developer' }}</em><br>
          用代码解决实际问题
        </h1>
        <div class="font-mono text-xs md:text-sm text-neon-green mt-3 md:mt-5 min-h-[22px]">
          {{ typedText }}<span class="animate-blink">▊</span>
        </div>
        <p class="text-text text-sm md:text-base mt-3 md:mt-5 leading-relaxed max-w-[480px]">
          {{ profile?.bio || '加载中...' }}
        </p>
        <!-- BUG-09 修复：移除Hero左侧的技术标签 -->
        <div class="cta mt-6 md:mt-8 flex flex-col md:flex-row gap-3 md:gap-4">
          <a
            href="#projects"
            class="btn-primary font-mono text-sm bg-neon-green text-[#050810] px-6 py-3 font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow"
            style="clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 100%, 0 100%);"
          >
            查看作品 →
          </a>
          <a
            href="#contact"
            class="btn-ghost font-mono text-sm text-neon-green border border-neon-green/30 px-6 py-3 hover:bg-neon-green/8 transition-colors"
            style="clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 100%, 0 100%);"
          >
            联系我
          </a>
        </div>
      </div>

      <!-- 右侧雷达 -->
      <div class="hero-right relative h-[420px] hidden md:block">
        <div class="radar-wrap absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[260px] h-[260px]">
          <div class="radar w-full h-full rounded-full border border-neon-green/15 relative radar-bg shadow-inner">
            <div class="radar-lines"></div>
            <div class="sweep absolute inset-0 rounded-full animate-sweep sweep-gradient"></div>
            <div class="radar-center absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-neon-green shadow-[0_0_12px_#00ffc8]"></div>
          </div>
          <!-- 环绕技术标签 -->
          <div class="orbit-tech absolute -top-3 left-1/2 -translate-x-1/2 flex items-center gap-2 text-xs text-text-bright">
            <span class="dot w-2 h-2 rounded-full bg-neon-green shadow-[0_0_8px_#00ffc8]"></span>
            <span>后端开发</span>
          </div>
          <div class="orbit-tech absolute top-8 -right-[70px] flex items-center gap-2 text-xs text-text-bright">
            <span class="dot w-2 h-2 rounded-full bg-[#4a9fff] shadow-[0_0_8px_#4a9fff]"></span>
            <span>自动化</span>
          </div>
          <div class="orbit-tech absolute bottom-10 -right-20 flex items-center gap-2 text-xs text-text-bright">
            <span class="dot w-2 h-2 rounded-full bg-neon-yellow shadow-[0_0_8px_#ffb020]"></span>
            <span>机器视觉</span>
          </div>
          <div class="orbit-tech absolute -bottom-5 left-1/2 -translate-x-1/2 flex items-center gap-2 text-xs text-text-bright">
            <span class="dot w-2 h-2 rounded-full bg-[#ff4d6d] shadow-[0_0_8px_#ff4d6d]"></span>
            <span>硬件交互</span>
          </div>
          <div class="orbit-tech absolute top-[70px] -left-[70px] flex items-center gap-2 text-xs text-text-bright">
            <span class="dot w-2 h-2 rounded-full bg-[#a78bfa] shadow-[0_0_8px_#a78bfa]"></span>
            <span>前端</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 坐标条 BUG-13 修复：移动端适配 -->
    <div class="hero-coord relative z-20 max-w-7xl mx-auto px-4 md:px-12 pb-8 pt-4 flex flex-col md:flex-row gap-2 md:gap-0 md:justify-between border-t border-line font-mono text-xs text-text-dim">
      <span>LAT <b class="text-neon-green">00.00°N</b> · LNG <b class="text-neon-green">000.00°E</b></span>
      <span>SIGNAL STRENGTH <b class="text-neon-green">▮▮▮▮▮▯▯ 72%</b></span>
      <span>UPTIME <b class="text-neon-green">99.9%</b></span>
    </div>

    <!-- 重点项目 BUG-13 修复：移动端适配 -->
    <section id="projects" class="section relative z-20 max-w-7xl mx-auto px-4 md:px-12 py-8 md:py-16">
      <div class="section-head flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-7">
        <h2 class="font-rajdhani text-2xl md:text-3xl text-text-bright tracking-wider">
          <span class="text-neon-green text-sm mr-3">// 01</span>SIGNAL.ARCHIVE · 重点项目
        </h2>
        <div class="tabs flex gap-0">
          <div
            v-for="cat in categories"
            :key="cat.value"
            @click="activeCategory = cat.value"
            :class="['tab font-mono text-xs px-3 md:px-5 py-2 cursor-pointer border transition-colors',
              activeCategory === cat.value ? 'text-neon-green border-neon-green/30 bg-neon-green/5' : 'text-text-dim border-transparent']"
          >
            {{ cat.label }}
          </div>
        </div>
      </div>

      <div class="cards grid grid-cols-2 md:grid-cols-3 gap-5">
        <div
          v-for="project in displayProjects"
          :key="project.id"
          @click="goToDetail(project.id)"
          class="card bg-bg-panel border border-line cursor-pointer transition-all duration-300 hover:border-neon-green hover:-translate-y-1 hover:shadow-[0_10px_30px_rgba(0,255,200,0.1)] overflow-hidden flex flex-col"
          style="clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px));"
        >
          <!-- BUG-07 修复：图片占60%，显示封面图 -->
          <!-- BUG-10 修复：移除 PRJ-XXX 标签，避免遮挡图片 -->
          <div class="cover relative overflow-hidden flex-[3]">
            <img
              v-if="project.cover_image"
              :src="project.cover_image"
              :alt="project.title"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full bg-gradient-to-br from-bg-panel to-bg-panel-2 flex items-center justify-center">
              <div class="font-mono text-xs text-text-dim">NO IMAGE</div>
            </div>
            <div class="cover-scan absolute inset-0 bg-gradient-to-r from-transparent via-neon-green/8 to-transparent -translate-x-full transition-transform duration-700"></div>
          </div>
          <!-- BUG-07 修复：文字占40% -->
          <div class="body p-5 flex-[2] flex flex-col">
            <!-- BUG-07 修复：标题字号更大 -->
            <div class="title font-rajdhani text-2xl text-text-bright font-semibold leading-tight">{{ project.title }}</div>
            <!-- BUG-07 修复：简介超过一行显示省略号 -->
            <div class="sum text-sm text-text mt-2 leading-relaxed line-clamp-1">{{ project.summary }}</div>
            <div class="techs mt-3 flex flex-wrap gap-1.5">
              <span
                v-for="tech in project.tech_stack.split(',')"
                :key="tech"
                class="font-mono text-[10px] text-neon-green border border-neon-green/30 px-2 py-0.5"
              >
                {{ tech }}
              </span>
            </div>
            <!-- BUG-07 修复：移除浏览量显示 -->
            <div class="foot mt-auto pt-3 border-t border-line flex justify-end font-mono text-xs text-text-dim">
              <span>{{ formatDate(project.created_at) }} →</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 显示更多按钮 (BUG-03 修复) -->
      <div v-if="hasMoreProjects" class="text-center mt-8">
        <button
          @click="toggleShowAll"
          class="font-mono text-sm text-neon-green border border-neon-green/30 px-6 py-3 hover:bg-neon-green/8 transition-colors"
          style="clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 100%, 0 100%);"
        >
          {{ showAllProjects ? '▲ 收起' : '▼ 显示更多' }} ({{ filteredProjectsCount }})
        </button>
      </div>
    </section>

    <!-- 终端页脚 BUG修复：增加底部padding -->
    <footer id="contact" class="terminal-footer relative z-20 mt-16 pb-8">
      <div class="term-window max-w-4xl mx-auto px-4 md:px-0 border border-line shadow-[0_20px_60px_rgba(0,0,0,0.5),0_0_40px_rgba(0,255,200,0.05)]">
        <div class="term-titlebar flex items-center gap-2 bg-[#1a2030] px-4 py-2.5 border-b border-line">
          <span class="t-dot w-3 h-3 rounded-full bg-[#ff5f57]"></span>
          <span class="t-dot w-3 h-3 rounded-full bg-[#febc2e]"></span>
          <span class="t-dot w-3 h-3 rounded-full bg-[#28c840]"></span>
          <span class="t-title flex-1 text-center font-mono text-xs text-text-dim">admin@red岸: ~/contact</span>
        </div>
        <div class="term-body bg-black px-7 py-6 font-mono text-sm leading-loose min-h-[280px]">
          <div class="line text-text"><span class="text-neon-green mr-2">$</span><span class="text-text-bright">whoami</span></div>
          <div class="line text-[#8899aa]"><span class="mr-2">→</span> 独立开发者 / 全栈 / 自动化方向</div>
          <div class="line">&nbsp;</div>
          <div class="line text-text"><span class="text-neon-green mr-2">$</span><span class="text-text-bright">contact --all</span></div>
          <div class="line text-[#8899aa]"><span class="text-text-dim mr-2">微信</span> {{ profile?.wechat || 'your_wechat' }}</div>
          <div class="line text-[#8899aa]"><span class="text-text-dim mr-2">邮箱</span> <a :href="`mailto:${profile?.email}`" class="text-neon-green border-b border-dashed border-neon-green/40">{{ profile?.email || 'hello@example.com' }}</a></div>
          <div class="line text-[#8899aa]"><span class="text-text-dim mr-2">GitHub</span> <a :href="profile?.github_url" target="_blank" class="text-neon-green border-b border-dashed border-neon-green/40">{{ profile?.github_url || 'github.com/your-id' }}</a></div>
          <div class="line">&nbsp;</div>
          <div class="line text-text"><span class="text-neon-green mr-2">$</span><span class="text-text-bright">echo "欢迎接单 · 远程协作 · 长期有效"</span></div>
          <div class="line text-neon-green">→ 终端就绪. 等待指令...</div>
          <div class="line text-text"><span class="text-neon-green mr-2">$</span><span class="inline-block w-2 h-4 bg-neon-green align-middle animate-blink"></span></div>
        </div>
      </div>
      <div class="term-bottom max-w-7xl mx-auto mt-5 px-12 pb-10 flex justify-between font-mono text-xs text-text-dim">
        <span>© 2026 {{ profile?.name || 'YOUR NAME' }} — Built with Vue3 + FastAPI</span>
        <span>v2.1 · BUILD 2026.10.20</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profile'
import { getProjects } from '@/api'

const router = useRouter()
const profileStore = useProfileStore()
const profile = computed(() => profileStore.profile)

// 鼠标光斑
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

// 打字机效果
const slogans = [
  '> 后端开发 · Python / FastAPI',
  '> 工业自动化 · 轨道信号检测效率提升 8 倍',
  '> 机器视觉 · OpenCV / 实时图像处理',
  '> 硬件交互 · 嵌入式 / 机械臂控制',
  '> 接外包 · 远程协作 · 长期有效'
]
const typedText = ref('')
let sloganIndex = 0
let charIndex = 0
let deleting = false
let typingTimer = null

const typeWriter = () => {
  const currentSlogan = slogans[sloganIndex]

  if (!deleting) {
    typedText.value = currentSlogan.slice(0, charIndex)
    charIndex++

    if (charIndex > currentSlogan.length) {
      deleting = true
      typingTimer = setTimeout(typeWriter, 1800)
      return
    }
    typingTimer = setTimeout(typeWriter, 60)
  } else {
    typedText.value = currentSlogan.slice(0, charIndex)
    charIndex--

    if (charIndex === 0) {
      deleting = false
      sloganIndex = (sloganIndex + 1) % slogans.length
    }
    typingTimer = setTimeout(typeWriter, 30)
  }
}

// 技术标签
const techTags = ref(['Python', 'Vue3', 'FastAPI', 'OpenCV', '工业自动化'])

// 分类切换
const categories = [
  { label: '[PROJECTS] 项目', value: 'project' },
  { label: '[WORKS] 作品', value: 'work' }
]
const activeCategory = ref('project')
const projects = ref([])
const showAllProjects = ref(false) // BUG-03 修复：控制是否显示全部

// BUG-03 修复：计算当前分类的项目列表
const filteredProjects = computed(() => {
  return projects.value.filter(p => p.category === activeCategory.value)
})

// BUG-03 修复：计算当前分类的项目数量
const filteredProjectsCount = computed(() => {
  return filteredProjects.value.length
})

// BUG-03 修复：判断是否有更多项目
const hasMoreProjects = computed(() => {
  return filteredProjects.value.length > 3
})

// BUG-03 修复：根据状态显示项目（初始3个或全部）
const displayProjects = computed(() => {
  if (showAllProjects.value) {
    return filteredProjects.value
  }
  return filteredProjects.value.slice(0, 3)
})

// BUG-03 修复：切换显示全部/收起
const toggleShowAll = () => {
  showAllProjects.value = !showAllProjects.value
}

// 获取项目数据
const fetchProjects = async () => {
  try {
    projects.value = await getProjects({ published: true })
  } catch (error) {
    console.error('获取项目列表失败:', error)
  }
}

// 跳转详情
const goToDetail = (id) => {
  router.push(`/project/${id}`)
}

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
}

// BUG-08 修复：导航跳转并切换分类
const scrollToProjects = (category) => {
  activeCategory.value = category
  showAllProjects.value = false
  const element = document.getElementById('projects')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
  typeWriter()
  profileStore.fetchProfile()
  fetchProjects()
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  if (typingTimer) clearTimeout(typingTimer)
})
</script>

<style scoped>
.bg-grid {
  background-image:
    linear-gradient(rgba(0,255,200,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,200,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

.radar-bg {
  background:
    radial-gradient(circle, transparent 18%, rgba(0,255,200,0.05) 19%, transparent 20%,
                    transparent 38%, rgba(0,255,200,0.05) 39%, transparent 40%,
                    transparent 58%, rgba(0,255,200,0.05) 59%, transparent 60%);
  box-shadow: inset 0 0 40px rgba(0,255,200,0.05);
}

.radar-lines::before,
.radar-lines::after {
  content: '';
  position: absolute;
  background: rgba(0,255,200,0.12);
}

.radar-lines::before {
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
}

.radar-lines::after {
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
}

.sweep-gradient {
  background: conic-gradient(from 0deg, rgba(0,255,200,0.35), transparent 70deg);
}

.card:hover .cover-scan {
  transform: translateX(100%);
}
</style>
