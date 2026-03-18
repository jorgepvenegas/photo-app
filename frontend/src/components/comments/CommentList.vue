<template>
  <div class="space-y-4">
    <div v-for="comment in commentsStore.comments" :key="comment.id" class="flex gap-3">
      <div class="flex-shrink-0">
        <div class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
          <span class="text-sm font-medium text-primary-700">
            {{ comment.user.email[0].toUpperCase() }}
          </span>
        </div>
      </div>
      
      <div class="flex-1 min-w-0">
        <div class="bg-gray-50 rounded-lg p-3">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-900">
              {{ comment.user.email }}
            </span>
            <span class="text-xs text-gray-500">
              {{ formatDate(comment.created_at) }}
            </span>
          </div>
          
          <p v-if="!comment.is_deleted" class="mt-1 text-sm text-gray-700">
            {{ comment.content }}
          </p>
          <p v-else class="mt-1 text-sm text-gray-400 italic">
            [deleted]
          </p>
        </div>
        
        <div v-if="!comment.is_deleted && comment.user_id === authStore.user?.id" class="mt-1 flex gap-2">
          <button
            @click="startEdit(comment)"
            class="text-xs text-gray-500 hover:text-gray-700"
          >
            Edit
          </button>
          <button
            @click="deleteComment(comment.id)"
            class="text-xs text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="commentsStore.loading" class="text-center py-4">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto"></div>
    </div>
    
    <div v-if="!commentsStore.loading && commentsStore.comments.length === 0" class="text-center py-8 text-gray-500">
      No comments yet. Be the first to comment!
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCommentsStore } from '@/stores/comments'
import { useAuthStore } from '@/stores/auth'
import type { Comment } from '@/types/comment'

const commentsStore = useCommentsStore()
const authStore = useAuthStore()

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const startEdit = (comment: Comment) => {
  // TODO: Implement inline editing
  const newContent = prompt('Edit your comment:', comment.content)
  if (newContent && newContent !== comment.content) {
    commentsStore.updateComment(comment.id, newContent)
  }
}

const deleteComment = (commentId: string) => {
  if (confirm('Are you sure you want to delete this comment?')) {
    commentsStore.deleteComment(commentId)
  }
}
</script>
