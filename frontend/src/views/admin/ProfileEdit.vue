<template>
  <div class="admin-profile-edit min-h-screen bg-[#050810]">
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
            个人信息编辑
          </div>
        </div>
      </div>

      <!-- 表单 -->
      <div class="max-w-3xl mx-auto px-8 py-8">
        <div v-if="loading" class="text-center py-16 font-mono text-neon-yellow">
          加载中...
        </div>

        <div v-else-if="error" class="text-center py-16 font-mono text-red-400">
          {{ error }}
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-6">
          <!-- 姓名 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 姓名/昵称 NAME</label>
            <input
              v-model="form.name"
              type="text"
              placeholder="Your Name"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              required
            />
          </div>

          <!-- 头像 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 头像 AVATAR</label>
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
              <div v-if="form.avatar_url" class="mt-4">
                <img :src="form.avatar_url" alt="头像预览" class="w-32 h-32 mx-auto rounded-full border border-line object-cover" />
              </div>
            </div>
          </div>

          <!-- 一句话简介 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 一句话简介 BIO</label>
            <textarea
              v-model="form.bio"
              placeholder="专注工业自动化、Python 工具链与全栈开发..."
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright text-sm outline-none focus:border-neon-yellow transition-colors resize-vertical"
              rows="3"
              required
            ></textarea>
          </div>

          <!-- 打字机文案 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// Hero 区打字机文案 TYPING_SLOGAN</label>
            <textarea
              v-model="form.typing_slogan"
              placeholder="> 后端开发 · Python / FastAPI"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors resize-vertical whitespace-pre-wrap"
              rows="3"
              required
            ></textarea>
            <div class="font-mono text-xs text-text-dim mt-1">提示：支持多行文案，首页将自动循环显示</div>
          </div>

          <!-- 联系方式 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 微信号 WECHAT</label>
            <input
              v-model="form.wechat"
              type="text"
              placeholder="your_wechat"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
            />
          </div>

          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 邮箱 EMAIL</label>
            <input
              v-model="form.email"
              type="email"
              placeholder="hello@example.com"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
            />
          </div>

          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// GitHub 链接 GITHUB_URL</label>
            <input
              v-model="form.github_url"
              type="url"
              placeholder="https://github.com/your-id"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
            />
          </div>

          <!-- 底部操作按钮 -->
          <div class="actions flex gap-4 pt-6 border-t border-line bg-bg-panel -mx-8 px-8 -mb-8 py-4 sticky bottom-0">
            <button
              type="button"
              @click="$router.push('/admin/projects')"
              class="flex-1 py-3 text-center font-mono text-sm text-text-dim border border-line hover:bg-line transition-colors"
              style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 py-3 text-center font-mono text-sm text-[#050810] bg-neon-green font-bold hover:shadow-[0_0_20px_rgba(0,255,200,0.4)] transition-shadow disabled:opacity-50"
              style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
            >
              {{ saving ? '保存中...' : '保 存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAdminProfile, updateProfile, uploadImage } from '@/api'

const router = useRouter()

const loading = ref(true)
const error = ref(null)
const saving = ref(false)
const uploadProgress = ref(0)

const fileInput = ref(null)

const form = ref({
  name: '',
  avatar_url: '',
  bio: '',
  typing_slogan: '',
  wechat: null,
  email: null,
  github_url: null
})

// 加载个人信息
const fetchProfile = async () => {
  try {
    loading.value = true
    const profile = await getAdminProfile()
    form.value = {
      name: profile.name,
      avatar_url: profile.avatar_url,
      bio: profile.bio,
      typing_slogan: profile.typing_slogan,
      wechat: profile.wechat,
      email: profile.email,
      github_url: profile.github_url
    }
  } catch (err) {
    error.value = err.detail || '加载个人信息失败'
  } finally {
    loading.value = false
  }
}

// 处理文件上传
const handleFileChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过 5MB')
    return
  }

  try {
    uploadProgress.value = 50
    const result = await uploadImage(file)
    form.value.avatar_url = result.url
    uploadProgress.value = 0
  } catch (err) {
    alert(err.detail || '上传失败')
    uploadProgress.value = 0
  }
}

// 提交表单
const handleSubmit = async () => {
  saving.value = true

  try {
    await updateProfile(form.value)
    alert('保存成功！')
    router.push('/admin/projects')
  } catch (err) {
    alert(err.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchProfile()
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
