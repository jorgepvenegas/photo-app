import apiClient from './client'
import type { Comment, CommentList, CreateCommentRequest, UpdateCommentRequest } from '@/types/comment'

export const commentsApi = {
  list: async (photoId: string, page = 1, perPage = 20): Promise<CommentList> => {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('per_page', perPage.toString())
    
    const response = await apiClient.get(`/photos/${photoId}/comments?${params.toString()}`)
    return response.data
  },

  create: async (photoId: string, data: CreateCommentRequest): Promise<Comment> => {
    const response = await apiClient.post(`/photos/${photoId}/comments`, data)
    return response.data
  },

  update: async (commentId: string, data: UpdateCommentRequest): Promise<Comment> => {
    const response = await apiClient.put(`/comments/${commentId}`, data)
    return response.data
  },

  delete: async (commentId: string) => {
    const response = await apiClient.delete(`/comments/${commentId}`)
    return response.data
  },
}
