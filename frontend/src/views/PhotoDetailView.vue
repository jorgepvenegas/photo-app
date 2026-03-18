<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    
    <main class="py-8">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-6">
          <router-link to="/feed" class="text-sm text-gray-600 hover:text-gray-900">
            ← Back to feed
          </router-link>
        </div>
        
        <div v-if="photosStore.currentPhoto" class="card">
          <!-- Photo -->
          <div class="relative">
            <img
              :src="photosStore.currentPhoto.storage_url"
              :alt="photosStore.currentPhoto.title"
              class="w-full h-auto object-cover"
            />
          </div>
          
          <!-- Photo info -->
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div>
                <h1 class="text-2xl font-bold text-gray-900">
                  {{ photosStore.currentPhoto.title }}
                </h1>
                <p class="mt-1 text-sm text-gray-500">
                  By {{ photosStore.currentPhoto.user.email }}
                </p>
              </div>
              <span
                v-if="!photosStore.currentPhoto.is_public"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
              >
                Private
              </span>
            </div>
            
            <p v-if="photosStore.currentPhoto.description" class="mt-4 text-gray-600">
              {{ photosStore.currentPhoto.description }}
            </p>
            
            <div class="mt-4 text-sm text-gray-500">
              {{ formatDate(photosStore.currentPhoto.created_at) }}
            </div>
          </div>
          
          <!-- Comments section -->
          <div class="border-t border-gray-200 p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-4">
              Comments ({{ photosStore.currentPhoto.comments_count }})
            </h2>
            <CommentForm @submit="handleAddComment" />
            <CommentList class="mt-6" />
          </div>
        </div>
        
        <div v-else-if="photosStore.loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Loading photo...</p>
        </div>
        
        <div v-else class="text-center py-12">
          <p class="text-gray-600">Photo not found</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { usePhotosStore } from '@/stores/photos'
import { useCommentsStore } from '@/stores/comments'
import AppHeader from '@/components/ui/AppHeader.vue'
import CommentList from '@/components/comments/CommentList.vue'
import CommentForm from '@/components/comments/CommentForm.vue'

const route = useRoute()
const photosStore = usePhotosStore()
const commentsStore = useCommentsStore()

const photoId = route.params.id as string

onMounted(() => {
  loadPhoto()
})

watch(() => route.params.id, () => {
  loadPhoto()
})

const loadPhoto = () => {
  photosStore.fetchPhoto(photoId)
  commentsStore.fetchComments(photoId)
}

const handleAddComment = async (content: string) => {
  await commentsStore.addComment(photoId, content)
  photosStore.currentPhoto!.comments_count++
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
