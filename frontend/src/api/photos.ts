import apiClient from './client'
import type { Photo, PhotoList, PhotoDetail, UploadRequest, PresignedUrlResponse, UploadConfirmRequest } from '@/types/photo'

export const photosApi = {
  list: async (page = 1, perPage = 20, userId?: string): Promise<PhotoList> => {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('per_page', perPage.toString())
    if (userId) params.append('user_id', userId)
    
    const response = await apiClient.get(`/photos?${params.toString()}`)
    return response.data
  },

  listMyPhotos: async (page = 1, perPage = 20): Promise<PhotoList> => {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('per_page', perPage.toString())
    
    const response = await apiClient.get(`/photos/me?${params.toString()}`)
    return response.data
  },

  get: async (id: string): Promise<PhotoDetail> => {
    const response = await apiClient.get(`/photos/${id}`)
    return response.data
  },

  update: async (id: string, data: Partial<Photo>) => {
    const response = await apiClient.put(`/photos/${id}`, data)
    return response.data
  },

  delete: async (id: string) => {
    const response = await apiClient.delete(`/photos/${id}`)
    return response.data
  },

  getPresignedUrl: async (data: UploadRequest): Promise<PresignedUrlResponse> => {
    const response = await apiClient.post('/upload/presigned-url', data)
    return response.data
  },

  confirmUpload: async (data: UploadConfirmRequest): Promise<Photo> => {
    const response = await apiClient.post('/upload/confirm', data)
    return response.data
  },
}
