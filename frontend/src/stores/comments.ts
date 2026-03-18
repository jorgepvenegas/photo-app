import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { commentsApi } from '@/api/comments'
import type { Comment, CommentList, CreateCommentRequest, UpdateCommentRequest } from '@/types/comment'

export const useCommentsStore = defineStore('comments', () => {
  // State
  const comments = ref<Comment[]>([])
  const totalComments = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const hasMoreComments = computed(() => {
    return comments.value.length < totalComments.value
  })

  // Actions
  const fetchComments = async (photoId: string, page = 1, perPage = 20) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await commentsApi.list(photoId, page, perPage)
      
      if (page === 1) {
        comments.value = response.comments
      } else {
        comments.value.push(...response.comments)
      }
      
      totalComments.value = response.total
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load comments'
      throw err
    } finally {
      loading.value = false
    }
  }

  const addComment = async (photoId: string, content: string) => {
    try {
      const comment = await commentsApi.create(photoId, { content })
      comments.value.unshift(comment)
      totalComments.value++
      return comment
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to add comment'
      throw err
    }
  }

  const updateComment = async (commentId: string, content: string) => {
    try {
      const updated = await commentsApi.update(commentId, { content })
      const index = comments.value.findIndex(c => c.id === commentId)
      if (index !== -1) {
        comments.value[index] = updated
      }
      return updated
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update comment'
      throw err
    }
  }

  const deleteComment = async (commentId: string) => {
    try {
      await commentsApi.delete(commentId)
      const index = comments.value.findIndex(c => c.id === commentId)
      if (index !== -1) {
        comments.value[index].is_deleted = true
        comments.value[index].content = '[deleted]'
      }
      totalComments.value--
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete comment'
      throw err
    }
  }

  const clearComments = () => {
    comments.value = []
    totalComments.value = 0
  }

  return {
    comments,
    totalComments,
    loading,
    error,
    hasMoreComments,
    fetchComments,
    addComment,
    updateComment,
    deleteComment,
    clearComments,
  }
})
