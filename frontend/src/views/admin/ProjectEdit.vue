<template>
  <div class="admin-project-edit min-h-screen bg-[#050810]">
    <!-- 全局网格背景 -->
    <div class="fixed inset-0 z-0 pointer-events-none bg-grid-admin"></div>

    <div class="relative z-20">
      <!-- 顶部栏 -->
      <div class="topbar flex justify-between items-center px-8 py-4 border-b border-line">
        <div class="flex items-center gap-4">
          <button
            @click="$router.push('/admin/projects')"
            class="font-mono text-xs text-text-dim hover:text-neon-yellow transition-colors"
          >
            ← 返回列表
          </button>
          <div class="font-rajdhani text-lg text-text-bright">
            {{ isEdit ? '编辑项目' : '新建项目' }}
            <span v-if="isEdit" class="font-mono text-sm text-neon-yellow ml-2">ID: {{ $route.params.id }}</span>
          </div>
        </div>
      </div>

      <!-- 表单 -->
      <div class="max-w-4xl mx-auto px-8 py-8">
        <div v-if="loading" class="text-center py-16 font-mono text-neon-yellow">
          加载中...
        </div>

        <div v-else-if="error" class="text-center py-16 font-mono text-red-400">
          {{ error }}
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 填写说明 -->
          <div class="border border-line bg-bg-panel/40 px-4 py-3 font-mono text-xs text-text-dim leading-relaxed">
            提示：草稿允许留空；发布前至少填写标题，简介、正文、封面、技术栈和链接都可以稍后补充。
          </div>

          <!-- 标题 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 标题 TITLE</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="项目标题（发布前必填）"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
            />
          </div>

          <!-- 简介 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 一句话简介 SUMMARY（可选）</label>
            <input
              v-model="form.summary"
              type="text"
              placeholder="列表卡片显示的一句话，可留空"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
            />
          </div>

          <!-- 分类和技术栈 -->
          <div class="grid grid-cols-2 gap-4">
            <div class="row">
              <label class="block font-mono text-xs text-text-dim mb-2">// 分类 CATEGORY</label>
              <select
                v-model="form.category"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              >
                <option value="project">项目 project</option>
                <option value="work">作品 work</option>
              </select>
            </div>

            <div class="row">
              <label class="block font-mono text-xs text-text-dim mb-2">// 技术栈 TAGS (逗号分隔)</label>
              <input
                v-model="form.tech_stack"
                type="text"
                placeholder="Python,Vue3,FastAPI"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              />
            </div>
          </div>

          <!-- 封面图 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 封面图 COVER</label>
            <div class="border border-dashed border-line p-6 text-center">
              <input
                type="file"
                @change="handleFileChange"
                accept="image/*"
                class="hidden"
                ref="fileInput"
              />
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="font-mono text-sm text-neon-green hover:underline"
              >
                拖拽或 <b>点击上传</b> （jpg/png/webp, ≤5MB）
              </button>
              <div v-if="uploadProgress" class="mt-2 font-mono text-xs text-neon-yellow">
                上传中... {{ uploadProgress }}%
              </div>
              <div v-if="form.cover_image" class="mt-4">
                <img :src="form.cover_image" alt="封面预览" class="max-h-40 mx-auto border border-line" />
                <button
                  type="button"
                  @click="form.cover_image = null"
                  class="mt-2 font-mono text-xs text-red-400 hover:underline"
                >
                  删除
                </button>
              </div>
            </div>
          </div>

          <!-- BUG-12 修复：项目多图上传 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 项目图片（多图） PROJECT_IMAGES</label>
            <div class="border border-line p-4">
              <input
                type="file"
                @change="handleMultipleImages"
                accept="image/*"
                multiple
                class="hidden"
                ref="multiImageInput"
              />
              <button
                type="button"
                @click="$refs.multiImageInput.click()"
                class="w-full py-3 text-center font-mono text-sm text-neon-green border border-neon-green/30 hover:bg-neon-green/10 transition-colors"
              >
                + 添加项目图片（可多选）
              </button>
              <div v-if="multiUploadProgress" class="mt-2 font-mono text-xs text-neon-yellow text-center">
                上传中... {{ multiUploadProgress }}%
              </div>
              <!-- 图片列表 -->
              <div v-if="form.project_images && form.project_images.length > 0" class="mt-4 grid grid-cols-3 gap-3">
                <div
                  v-for="(img, index) in form.project_images"
                  :key="index"
                  class="relative border border-line group"
                >
                  <img :src="img" :alt="`图片${index+1}`" class="w-full h-32 object-cover" />
                  <button
                    type="button"
                    @click="removeProjectImage(index)"
                    class="absolute top-1 right-1 w-6 h-6 bg-red-500/80 text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    ×
                  </button>
                  <div class="absolute bottom-0 left-0 right-0 bg-black/60 text-center py-1 text-xs text-white font-mono">
                    {{ index + 1 }}
                  </div>
                </div>
              </div>
            </div>
            <div class="font-mono text-xs text-text-dim mt-1">
              提示：支持多张图片，详情页将显示轮播图
            </div>
          </div>

          <!-- 链接 -->
          <div class="grid grid-cols-2 gap-4">
            <div class="row">
              <label class="block font-mono text-xs text-text-dim mb-2">// 演示链接</label>
              <input
                v-model="form.demo_url"
                type="url"
                placeholder="https://"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              />
            </div>

            <div class="row">
              <label class="block font-mono text-xs text-text-dim mb-2">// GitHub 链接</label>
              <input
                v-model="form.github_url"
                type="url"
                placeholder="https://github.com/"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              />
            </div>
          </div>

          <!-- 排序 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 排序权重 SORT_ORDER (数字越小越靠前)</label>
            <input
              v-model.number="form.sort_order"
              type="number"
              placeholder="999"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
            />
          </div>

          <!-- 正文编辑器（Markdown + 实时预览） -->
          <div class="row">
            <div class="flex items-center justify-between gap-3 mb-2">
              <label class="block font-mono text-xs text-text-dim">// 正文 CONTENT（Markdown，可选）</label>
              <div class="flex font-mono text-[10px] border border-line">
                <button
                  type="button"
                  @click="editorMode = 'edit'"
                  :class="['px-3 py-1 transition-colors', editorMode === 'edit' ? 'bg-neon-yellow text-[#050810]' : 'text-text-dim hover:text-neon-yellow']"
                >
                  编辑
                </button>
                <button
                  type="button"
                  @click="editorMode = 'split'"
                  :class="['hidden md:block px-3 py-1 border-l border-line transition-colors', editorMode === 'split' ? 'bg-neon-yellow text-[#050810]' : 'text-text-dim hover:text-neon-yellow']"
                >
                  分栏
                </button>
                <button
                  type="button"
                  @click="editorMode = 'preview'"
                  :class="['px-3 py-1 border-l border-line transition-colors', editorMode === 'preview' ? 'bg-neon-yellow text-[#050810]' : 'text-text-dim hover:text-neon-yellow']"
                >
                  预览
                </button>
              </div>
            </div>

            <div :class="editorMode === 'split' ? 'grid md:grid-cols-2 gap-3' : ''">
              <!-- 编辑区 -->
              <div v-show="editorMode !== 'preview'" class="min-w-0">
                <div class="editor-bar flex gap-3 px-4 py-2 bg-bg-panel border border-line border-b-0 font-mono text-xs text-text-dim">
                  <button type="button" @click="insertMarkdown('**', '**')" class="hover:text-neon-yellow">B</button>
                  <button type="button" @click="insertMarkdown('*', '*')" class="hover:text-neon-yellow italic">I</button>
                  <button type="button" @click="insertMarkdown('# ', '')" class="hover:text-neon-yellow">H1</button>
                  <button type="button" @click="insertMarkdown('## ', '')" class="hover:text-neon-yellow">H2</button>
                  <button type="button" @click="insertMarkdown('`', '`')" class="hover:text-neon-yellow">&lt;&gt;</button>
                </div>
                <textarea
                  v-model="form.content"
                  ref="contentArea"
                  data-test="content-input"
                  placeholder="# 项目概述&#10;&#10;在这里写项目正文..."
                  class="w-full bg-[#050810] border border-line px-4 py-3 text-text font-mono text-sm outline-none focus:border-neon-yellow transition-colors resize-vertical"
                  rows="15"
                ></textarea>
              </div>

              <!-- 预览区 -->
              <div v-show="editorMode !== 'edit'" class="min-w-0">
                <div class="flex items-center justify-between px-4 py-2 bg-bg-panel border border-line border-b-0 font-mono text-xs text-text-dim">
                  <span>PREVIEW</span>
                  <span class="text-[10px]">实时渲染结果</span>
                </div>
                <div
                  data-test="markdown-preview"
                  class="markdown-body bg-[#050810] border border-line px-4 py-3 min-h-[320px] max-h-[560px] overflow-auto"
                  v-html="renderedPreview"
                ></div>
              </div>
            </div>

            <div class="font-mono text-xs text-text-dim mt-1">
              提示：使用 Markdown 编写，预览会实时更新；支持标题、列表、代码块、链接、图片、表格等。
            </div>
          </div>

          <!-- 底部操作按钮 -->
          <div class="actions flex gap-4 pt-6 border-t border-line bg-bg-panel -mx-8 px-8 -mb-8 py-4 sticky bottom-0">
            <button
              v-if="!isEdit || !projectData.is_published"
              type="button"
              @click="saveDraft"
              :disabled="saving"
              class="flex-1 py-3 text-center font-mono text-sm text-neon-yellow border border-neon-yellow hover:bg-neon-yellow/10 transition-colors disabled:opacity-50"
              style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
            >
              {{ saving ? '保存中...' : '□ 存草稿' }}
            </button>
            <button
              v-if="!isEdit || !projectData.is_published"
              type="button"
              @click="publishProject"
              :disabled="saving"
              class="flex-1 py-3 text-center font-mono text-sm text-[#050810] bg-neon-green font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow disabled:opacity-50"
              style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
            >
              {{ saving ? '发布中...' : '▶ 发 布' }}
            </button>
            <button
              v-if="isEdit && projectData.is_published"
              type="button"
              @click="saveChanges"
              :disabled="saving"
              class="flex-1 py-3 text-center font-mono text-sm text-[#050810] bg-neon-green font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow disabled:opacity-50"
              style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
            >
              {{ saving ? '保存中...' : '✓ 保 存' }}
            </button>
            <button
              v-if="isEdit && projectData.is_published"
              type="button"
              @click="unpublishProject"
              :disabled="saving"
              class="flex-1 py-3 text-center font-mono text-sm text-red-400 border border-red-400 hover:bg-red-400/10 transition-colors disabled:opacity-50"
              style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
            >
              {{ saving ? '处理中...' : '✗ 取消发布' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { getAdminProjectDetail, createProject, updateProject, uploadImage } from '@/api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const error = ref(null)
const saving = ref(false)
const uploadProgress = ref(0)

const fileInput = ref(null)
const multiImageInput = ref(null) // BUG-12 修复：多图上传引用
const multiUploadProgress = ref(0) // BUG-12 修复：多图上传进度
const contentArea = ref(null)

// 存储原始项目数据（用于判断当前发布状态）
const projectData = ref({
  is_published: false
})

const form = ref({
  title: '',
  summary: '',
  content: '',
  cover_image: null,
  tech_stack: '',
  demo_url: null,
  github_url: null,
  category: 'project',
  sort_order: 999,
  project_images: [] // BUG-12 修复：项目图片数组
})

// Markdown 实时预览
const editorMode = ref('edit')
const renderedPreview = computed(() => {
  if (!form.value.content || !form.value.content.trim()) {
    return '<p style="color:#5a6b85">暂无内容</p>'
  }
  return DOMPurify.sanitize(marked(form.value.content))
})

// 加载项目数据（编辑模式）
const fetchProject = async () => {
  try {
    loading.value = true
    // BUG-06 修复：使用管理端 API，不增加浏览量
    const project = await getAdminProjectDetail(route.params.id)
    projectData.value = project
    form.value = {
      title: project.title,
      summary: project.summary,
      content: project.content,
      cover_image: project.cover_image,
      tech_stack: project.tech_stack,
      demo_url: project.demo_url,
      github_url: project.github_url,
      category: project.category,
      sort_order: project.sort_order,
      project_images: project.project_images || [] // BUG-12 修复：加载项目图片
    }
  } catch (err) {
    error.value = err.detail || '加载项目失败'
  } finally {
    loading.value = false
  }
}

// 处理文件上传
const handleFileChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  // 验证文件大小
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过 5MB')
    return
  }

  try {
    uploadProgress.value = 50
    const result = await uploadImage(file)
    form.value.cover_image = result.url
    uploadProgress.value = 0
  } catch (err) {
    alert(formatError(err, '上传失败'))
    uploadProgress.value = 0
  }
}

// BUG-12 修复：处理多图上传
const handleMultipleImages = async (e) => {
  const files = Array.from(e.target.files)
  if (files.length === 0) return

  // 验证文件大小
  for (const file of files) {
    if (file.size > 5 * 1024 * 1024) {
      alert(`文件 ${file.name} 大小超过 5MB`)
      return
    }
  }

  try {
    multiUploadProgress.value = 10
    const uploadedUrls = []

    for (let i = 0; i < files.length; i++) {
      const result = await uploadImage(files[i])
      uploadedUrls.push(result.url)
      multiUploadProgress.value = Math.floor((i + 1) / files.length * 100)
    }

    // 添加到现有图片数组
    if (!form.value.project_images) {
      form.value.project_images = []
    }
    form.value.project_images.push(...uploadedUrls)

    multiUploadProgress.value = 0
    e.target.value = '' // 清空输入框，允许重复上传
  } catch (err) {
    alert(formatError(err, '上传失败'))
    multiUploadProgress.value = 0
  }
}

// BUG-12 修复：删除项目图片
const removeProjectImage = (index) => {
  form.value.project_images.splice(index, 1)
}

// 插入 Markdown 格式
const insertMarkdown = (before, after) => {
  const textarea = contentArea.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const text = form.value.content
  const selectedText = text.substring(start, end)

  form.value.content = text.substring(0, start) + before + selectedText + after + text.substring(end)

  // 重新聚焦并设置光标位置
  setTimeout(() => {
    textarea.focus()
    textarea.setSelectionRange(start + before.length, end + before.length)
  }, 0)
}

// 统一解析后端错误（FastAPI 校验错误 detail 可能是数组）
const formatError = (err, fallback = '保存失败') => {
  if (Array.isArray(err?.detail)) {
    return err.detail.map((item) => item.msg || '参数校验失败').join('\n')
  }
  return err?.detail || fallback
}

// 表单内回车不触发隐式提交，避免误发布
const handleSubmit = () => {}

// 提交数据的通用函数
const submitData = async (isPublished) => {
  const title = form.value.title.trim()

  // 草稿允许留空；发布只强制要求标题
  if (isPublished && !title) {
    alert('发布前请至少填写项目标题')
    return
  }

  saving.value = true

  try {
    const data = {
      ...form.value,
      title,
      is_published: isPublished
    }

    if (isEdit.value) {
      await updateProject(route.params.id, data)
    } else {
      await createProject(data)
    }

    const message = isPublished ? '发布成功！' : '草稿已保存'
    alert(message)
    router.push('/admin/projects')
  } catch (err) {
    alert(formatError(err))
  } finally {
    saving.value = false
  }
}

// 存草稿（BUG-01 修复：明确传递 false）
const saveDraft = () => {
  submitData(false)
}

// 发布项目（BUG-01 修复：明确传递 true）
const publishProject = () => {
  submitData(true)
}

// 保存已发布项目的修改（BUG-02 修复：保持发布状态）
const saveChanges = () => {
  submitData(true)
}

// 取消发布（BUG-02 修复：改为草稿状态）
const unpublishProject = () => {
  if (confirm('确定要取消发布吗？取消后将变为草稿状态。')) {
    submitData(false)
  }
}

onMounted(() => {
  if (isEdit.value) {
    fetchProject()
  }
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
