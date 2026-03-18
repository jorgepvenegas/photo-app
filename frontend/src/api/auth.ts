import apiClient from './client'
import type { User, LoginCredentials, RegisterCredentials } from '@/types/user'

export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const params = new URLSearchParams()
    params.append('username', credentials.email)
    params.append('password', credentials.password)
    
    const response = await apiClient.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  register: async (credentials: RegisterCredentials) => {
    const response = await apiClient.post('/auth/register', {
      email: credentials.email,
      password: credentials.password,
    })
    return response.data
  },

  logout: async () => {
    const response = await apiClient.post('/auth/logout')
    return response.data
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me')
    return response.data
  },

  verifyEmail: async (token: string) => {
    const response = await apiClient.get(`/auth/verify?token=${token}`)
    return response.data
  },

  forgotPassword: async (email: string) => {
    const response = await apiClient.post('/auth/forgot-password', { email })
    return response.data
  },

  resetPassword: async (token: string, password: string) => {
    const response = await apiClient.post('/auth/reset-password', {
      token,
      password,
    })
    return response.data
  },
}
