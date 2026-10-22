<template>
  <div class="login min-h-screen bg-[#050810] flex items-center justify-center">
    <!-- 全局网格背景 -->
    <div class="fixed inset-0 z-0 pointer-events-none bg-grid-admin"></div>

    <div class="relative z-20 w-full max-w-md px-8">
      <!-- 登录卡片 -->
      <div
        class="login-box bg-bg-panel/90 border border-neon-yellow/30 p-8"
        style="clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px));"
      >
        <!-- 标识 -->
        <div class="lock text-center font-mono text-xs text-neon-yellow tracking-[2px] mb-2">
          ▣ AUTHORIZED.ONLY
        </div>

        <!-- 标题 -->
        <h1 class="title text-center font-rajdhani text-2xl text-text-bright tracking-[3px] mb-1">
          红岸控制台
        </h1>

        <!-- 分隔线 -->
        <div class="divider text-center font-mono text-[10px] text-text-dim my-6">
          — 请通过身份验证 —
        </div>

        <!-- 错误提示 -->
        <div
          v-if="error"
          class="error-msg bg-red-900/20 border border-red-500/30 text-red-400 text-sm px-4 py-2 mb-4 font-mono"
        >
          {{ error }}
        </div>

        <!-- 表单 -->
        <form @submit.prevent="handleLogin">
          <div class="field mb-4">
            <label class="block font-mono text-[10px] text-text-dim mb-2">// USERNAME</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="admin"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              required
            />
          </div>

          <div class="field mb-6">
            <label class="block font-mono text-[10px] text-text-dim mb-2">// PASSWORD</label>
            <input
              v-model="form.password"
              type="password"
              placeholder="••••••••"
              class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
              required
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="login-btn w-full py-3 text-center bg-neon-yellow text-[#050810] font-mono text-sm font-bold tracking-[2px] hover:shadow-[0_0_20px_rgba(255,176,32,0.4)] transition-shadow disabled:opacity-50"
            style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
          >
            {{ loading ? '验证中...' : '>>> 验 证' }}
          </button>
        </form>
      </div>

      <!-- 返回公开站点 -->
      <div class="back-to-site text-center mt-6 font-mono text-xs text-text-dim">
        ← 返回 <button @click="$router.push('/')" class="text-neon-green hover:underline">公开站点</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { login } from '@/api'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref(null)

const handleLogin = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await login(form.value)
    authStore.setToken(response.access_token)
    router.push('/admin/projects')
  } catch (err) {
    error.value = err.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.bg-grid-admin {
  background-image:
    linear-gradient(rgba(255,176,32,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,176,32,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}
</style>
