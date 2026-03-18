<template>
  <form @submit.prevent="handleSubmit" class="flex gap-3">
    <div class="flex-shrink-0">
      <div class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
        <span class="text-sm font-medium text-primary-700">
          {{ authStore.user?.email[0].toUpperCase() }}
        </span>
      </div>
    </div>
    
    <div class="flex-1">
      <textarea
        v-model="content"
        rows="2"
        placeholder="Add a comment..."
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm resize-none"
        :disabled="loading"
      ></textarea>
      
      <div class="mt-2 flex items-center justify-between">
        <span class="text-xs text-gray-500">
          {{ content.length }}/2000 characters
        </span>
        
        <button
          type="submit"
          :disabled="!content.trim() || loading || content.length > 2000"
          class="btn-primary text-sm py-1 px-4"
        >
          <span v-if="loading">Posting...</span>
          <span v-else>Post Comment</span>
        </button>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const content = ref('')
const loading = ref(false)

const emit = defineEmits<{
  (e: 'submit', content: string): void
}>()

const handleSubmit = async () => {
  if (!content.value.trim()) return
  
  loading.value = true
  try {
    await emit('submit', content.value.trim())
    content.value = ''
  } finally {
    loading.value = false
  }
}
</script>
