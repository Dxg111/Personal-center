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
        <router-link
          to="/admin/password"
          class="font-mono text-xs text-text-dim hover:text-neon-yellow transition-colors"
        >
          修改密码
        </router-link>
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

          <!-- BUG-11 修复：雷达图技能标签管理 -->
          <div class="row">
            <label class="block font-mono text-xs text-text-dim mb-2">// 雷达图技能标签 RADAR_SKILLS</label>
            <div class="border border-line p-4 space-y-3">
              <div
                v-for="(skill, index) in form.radar_skills"
                :key="index"
                class="flex gap-2 items-center"
              >
                <input
                  v-model="skill.name"
                  type="text"
                  placeholder="技能名称"
                  class="flex-1 bg-[#050810] border border-line px-3 py-2 text-text-bright text-sm outline-none focus:border-neon-yellow"
                />
                <input
                  v-model="skill.color"
                  type="color"
                  class="w-16 h-10 border border-line cursor-pointer"
                />
                <select
                  v-model="skill.position"
                  class="bg-[#050810] border border-line px-3 py-2 text-text-bright text-sm outline-none focus:border-neon-yellow"
                >
                  <option value="top">顶部</option>
                  <option value="top-right">右上</option>
                  <option value="bottom-right">右下</option>
                  <option value="bottom">底部</option>
                  <option value="bottom-left">左下</option>
                  <option value="top-left">左上</option>
                </select>
                <button
                  type="button"
                  @click="removeSkill(index)"
                  class="px-3 py-2 text-red-400 border border-red-400/30 hover:bg-red-400/10 text-sm"
                >
                  删除
                </button>
              </div>
              <button
                type="button"
                @click="addSkill"
                class="w-full py-2 text-center font-mono text-sm text-neon-green border border-neon-green/30 hover:bg-neon-green/10 transition-colors"
              >
                + 添加技能标签
              </button>
            </div>
            <div class="font-mono text-xs text-text-dim mt-1">
              提示：最多6个技能标签，将显示在首页雷达图周围
            </div>
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
  github_url: null,
  // BUG-11 修复：雷达图技能标签
  radar_skills: []
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
      github_url: profile.github_url,
      // BUG-11 修复：加载雷达图技能标签
      radar_skills: profile.radar_skills || [
        { name: '后端开发', color: '#00ffc8', position: 'top' },
        { name: '自动化', color: '#4a9fff', position: 'top-right' },
        { name: '机器视觉', color: '#ffb020', position: 'bottom-right' },
        { name: '硬件交互', color: '#ff4d6d', position: 'bottom' },
        { name: '前端', color: '#a78bfa', position: 'top-left' }
      ]
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

// BUG-11 修复：添加技能标签
const addSkill = () => {
  if (form.value.radar_skills.length >= 6) {
    alert('最多只能添加6个技能标签')
    return
  }
  form.value.radar_skills.push({
    name: '',
    color: '#00ffc8',
    position: 'top'
  })
}

// BUG-11 修复：删除技能标签
const removeSkill = (index) => {
  form.value.radar_skills.splice(index, 1)
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
