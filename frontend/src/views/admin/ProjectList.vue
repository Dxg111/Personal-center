<template>
  <div class="admin-projects min-h-screen bg-[#050810]">
    <!-- 全局网格背景 -->
    <div class="fixed inset-0 z-0 pointer-events-none bg-grid-admin"></div>

    <div class="relative z-20">
      <!-- 顶部栏 -->
      <div class="topbar flex justify-between items-center px-8 py-4 border-b border-line bg-neon-yellow/5">
        <div class="brand font-rajdhani text-base text-text-bright tracking-wider">
          RED岸 <span class="text-neon-yellow">// CONSOLE</span>
        </div>
        <div class="flex items-center gap-6">
          <router-link
            to="/admin/profile"
            class="font-mono text-xs text-text-dim hover:text-neon-yellow transition-colors"
          >
            个人信息
          </router-link>
          <button
            @click="handleLogout"
            class="font-mono text-xs text-text-dim hover:text-neon-yellow transition-colors"
          >
            admin ▾ 退出
          </button>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="stats grid grid-cols-3 gap-px bg-line max-w-7xl mx-auto mt-8">
        <div class="stat bg-bg-panel p-6 text-center">
          <div class="n font-rajdhani text-3xl font-bold text-text-bright">{{ stats.total }}</div>
          <div class="l font-mono text-xs text-text-dim mt-1">TOTAL 总数</div>
        </div>
        <div class="stat bg-bg-panel p-6 text-center">
          <div class="n font-rajdhani text-3xl font-bold text-neon-green">{{ stats.published }}</div>
          <div class="l font-mono text-xs text-text-dim mt-1">PUBLISHED 已发布</div>
        </div>
        <div class="stat bg-bg-panel p-6 text-center">
          <div class="n font-rajdhani text-3xl font-bold text-neon-yellow">{{ stats.draft }}</div>
          <div class="l font-mono text-xs text-text-dim mt-1">DRAFT 草稿</div>
        </div>
      </div>

      <!-- 工具栏 -->
      <div class="toolbar flex justify-between items-center px-8 py-4 max-w-7xl mx-auto">
        <div class="title font-mono text-xs text-text">ALL PROJECTS — 全部项目</div>
        <button
          @click="$router.push('/admin/projects/new')"
          class="new-btn font-mono text-xs text-[#050810] bg-neon-green px-5 py-2 font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow"
          style="clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 100%, 0 100%);"
        >
          + 新建
        </button>
      </div>

      <!-- 项目列表 -->
      <div class="max-w-7xl mx-auto px-8 pb-16">
        <div v-if="loading" class="text-center py-16 font-mono text-neon-yellow">
          加载中...
        </div>

        <div v-else-if="error" class="text-center py-16 font-mono text-red-400">
          {{ error }}
        </div>

        <div v-else-if="projects.length === 0" class="text-center py-16 font-mono text-text-dim">
          暂无项目，点击"+ 新建"创建第一个项目
        </div>

        <table v-else class="list w-full border-collapse">
          <thead>
            <tr class="border-b border-line">
              <th class="text-left py-3 px-4 font-mono text-xs text-text-dim font-normal">标题</th>
              <th class="text-left py-3 px-4 font-mono text-xs text-text-dim font-normal">分类</th>
              <th class="text-left py-3 px-4 font-mono text-xs text-text-dim font-normal">状态</th>
              <th class="text-left py-3 px-4 font-mono text-xs text-text-dim font-normal">浏览</th>
              <th class="text-left py-3 px-4 font-mono text-xs text-text-dim font-normal">创建时间</th>
              <th class="text-left py-3 px-4 font-mono text-xs text-text-dim font-normal">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="project in projects"
              :key="project.id"
              class="border-b border-bg-panel hover:bg-bg-panel/30 transition-colors"
            >
              <td class="py-4 px-4 text-text-bright text-sm">{{ project.title || '（未命名草稿）' }}</td>
              <td class="py-4 px-4 text-text text-sm">{{ project.category === 'project' ? '项目' : '作品' }}</td>
              <td class="py-4 px-4">
                <span
                  :class="['badge font-mono text-[10px] px-2 py-1 border',
                    project.is_published
                      ? 'text-neon-green border-neon-green/40'
                      : 'text-neon-yellow border-neon-yellow/40']"
                >
                  {{ project.is_published ? '已发布' : '草稿' }}
                </span>
              </td>
              <td class="py-4 px-4 text-text text-sm">{{ project.views_count }}</td>
              <td class="py-4 px-4 text-text-dim text-sm font-mono text-xs">{{ formatDate(project.created_at) }}</td>
              <td class="py-4 px-4">
                <div class="ops font-mono text-xs flex gap-4">
                  <button
                    @click="handleEdit(project.id)"
                    class="text-neon-green hover:underline"
                  >
                    编辑
                  </button>
                  <button
                    @click="handleTogglePublish(project)"
                    class="text-neon-yellow hover:underline"
                  >
                    {{ project.is_published ? '取消发布' : '发布' }}
                  </button>
                  <button
                    @click="handleDelete(project)"
                    class="text-red-400 hover:underline"
                  >
                    删除
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getAdminProjects, deleteProject, togglePublish } from '@/api'

const router = useRouter()
const authStore = useAuthStore()

const projects = ref([])
const loading = ref(true)
const error = ref(null)

// 统计数据
const stats = computed(() => ({
  total: projects.value.length,
  published: projects.value.filter(p => p.is_published).length,
  draft: projects.value.filter(p => !p.is_published).length
}))

// 获取项目列表
const fetchProjects = async () => {
  try {
    loading.value = true
    error.value = null
    projects.value = await getAdminProjects()
  } catch (err) {
    error.value = err.detail || '获取项目列表失败'
  } finally {
    loading.value = false
  }
}

// 编辑项目
const handleEdit = (id) => {
  router.push(`/admin/projects/${id}/edit`)
}

// 切换发布状态
const handleTogglePublish = async (project) => {
  if (!project.is_published && !project.title.trim()) {
    alert('发布前请先编辑并填写标题')
    return
  }

  if (!confirm(`确定${project.is_published ? '取消发布' : '发布'}该项目吗？`)) {
    return
  }

  try {
    await togglePublish(project.id, !project.is_published)
    await fetchProjects()
  } catch (err) {
    alert(err.detail || '操作失败')
  }
}

// 删除项目
const handleDelete = async (project) => {
  const name = project.title || '未命名草稿'
  if (!confirm(`确定删除项目"${name}"吗？此操作不可恢复。`)) {
    return
  }

  try {
    await deleteProject(project.id)
    await fetchProjects()
  } catch (err) {
    alert(err.detail || '删除失败')
  }
}

// 退出登录
const handleLogout = () => {
  if (confirm('确定退出登录吗？')) {
    authStore.clearToken()
    router.push('/admin/login')
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.bg-grid-admin {
  background-image:
    linear-gradient(rgba(255,176,32,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,176,32,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}
</style>
