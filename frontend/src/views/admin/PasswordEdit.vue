<template>
  <div class="admin-password min-h-screen bg-[#050810]">
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
            修改密码
          </div>
        </div>
      </div>

      <div class="max-w-md mx-auto px-6 py-12">
        <div
          class="border border-line bg-bg-panel/80 p-8"
          style="clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px));"
        >
          <div class="font-mono text-[10px] text-neon-yellow tracking-[2px] mb-2">
            ▣ ACCOUNT.SECURITY
          </div>
          <h1 class="font-rajdhani text-2xl text-text-bright mb-6 tracking-wide">
            管理员密码
          </h1>

          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div>
              <label class="block font-mono text-xs text-text-dim mb-2">
                // 当前密码 CURRENT_PASSWORD
              </label>
              <input
                v-model="form.current_password"
                data-test="current-password"
                type="password"
                autocomplete="current-password"
                placeholder="输入当前登录密码"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
                required
              />
            </div>

            <div>
              <label class="block font-mono text-xs text-text-dim mb-2">
                // 新密码 NEW_PASSWORD（至少 8 位）
              </label>
              <input
                v-model="form.new_password"
                data-test="new-password"
                type="password"
                autocomplete="new-password"
                minlength="8"
                placeholder="至少 8 位"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
                required
              />
            </div>

            <div>
              <label class="block font-mono text-xs text-text-dim mb-2">
                // 确认新密码 CONFIRM_PASSWORD
              </label>
              <input
                v-model="form.confirm_password"
                data-test="confirm-password"
                type="password"
                autocomplete="new-password"
                placeholder="再次输入新密码"
                class="w-full bg-[#050810] border border-line px-4 py-3 text-text-bright font-mono text-sm outline-none focus:border-neon-yellow transition-colors"
                required
              />
            </div>

            <div class="font-mono text-xs text-text-dim leading-relaxed border border-line bg-[#050810] px-4 py-3">
              修改成功后当前登录会失效，需要使用新密码重新登录。
            </div>

            <div class="flex gap-4 pt-2">
              <button
                type="button"
                @click="cancel"
                class="flex-1 py-3 text-center font-mono text-sm text-text-dim border border-line hover:bg-line transition-colors"
                style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="flex-1 py-3 text-center font-mono text-sm text-[#050810] bg-neon-yellow font-bold hover:shadow-[0_0_20px_rgba(255,176,32,0.4)] transition-shadow disabled:opacity-50"
                style="clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);"
              >
                {{ saving ? '提交中...' : '确认修改' }}
              </button>
            </div>
          </form>
        </div>

        <div class="font-mono text-xs text-text-dim mt-4 leading-relaxed">
          提示：如果之后重建数据库，请同步更新 backend/.env.production 文件中的 ADMIN_PASSWORD。
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { changePassword } from '@/api'

const router = useRouter()
const authStore = useAuthStore()

const saving = ref(false)
const form = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const formatError = (err) => {
  if (Array.isArray(err?.detail)) {
    return err.detail.map((item) => item.msg || '参数校验失败').join('\n')
  }
  return err?.detail || '密码修改失败'
}

const cancel = () => {
  form.value = {
    current_password: '',
    new_password: '',
    confirm_password: ''
  }
  router.push('/admin/projects')
}

const handleSubmit = async () => {
  const current = form.value.current_password
  const next = form.value.new_password
  const confirm = form.value.confirm_password

  if (next.length < 8) {
    alert('新密码至少需要 8 位')
    return
  }

  if (next !== confirm) {
    alert('两次输入的新密码不一致')
    return
  }

  if (next === current) {
    alert('新密码不能与当前密码相同')
    return
  }

  saving.value = true

  try {
    await changePassword({
      current_password: current,
      new_password: next
    })

    authStore.clearToken()
    alert('密码修改成功，请使用新密码重新登录')
    router.push('/admin/login')
  } catch (err) {
    alert(formatError(err))
  } finally {
    saving.value = false
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
