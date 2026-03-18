import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, LoginCredentials, RegisterCredentials } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isVerified = computed(() => user.value?.is_verified ?? false)

  // Actions
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const clearToken = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  const fetchUser = async () => {
    try {
      const userData = await authApi.getMe()
      user.value = userData
      return userData
    } catch (err) {
      clearToken()
      throw err
    }
  }

  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.login(credentials)
      setToken(response.access_token)
      await fetchUser()
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const register = async (credentials: RegisterCredentials) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.register(credentials)
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    authApi.logout().catch(() => {}) // Ignore errors
    clearToken()
  }

  const verifyEmail = async (token: string) => {
    return await authApi.verifyEmail(token)
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isVerified,
    login,
    register,
    logout,
    fetchUser,
    verifyEmail,
    setToken,
    clearToken,
  }
})
