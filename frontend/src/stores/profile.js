import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProfile } from '@/api'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchProfile = async () => {
    loading.value = true
    error.value = null
    try {
      profile.value = await getProfile()
    } catch (err) {
      error.value = err.detail || '获取个人信息失败'
      console.error('获取个人信息失败:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    profile,
    loading,
    error,
    fetchProfile
  }
})
