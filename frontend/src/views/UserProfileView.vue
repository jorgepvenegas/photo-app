<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    
    <main class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Loading profile...</p>
        </div>
        
        <template v-else-if="user">
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">{{ user.email }}</h1>
            <p class="mt-2 text-gray-600">Member since {{ formatDate(user.created_at) }}</p>
          </div>
          
          <div>
            <h2 class="text-xl font-bold text-gray-900 mb-6">Photos</h2>
            <PhotoGrid
              :photos="photosStore.photos"
              :loading="photosStore.loading"
              @load-more="loadMore"
            />
            
            <div v-if="photosStore.photos.length === 0 && !photosStore.loading" class="text-center py-12 text-gray-500">
              This user hasn't uploaded any photos yet.
            </div>
          </div>
        </template>
        
        <div v-else class="text-center py-12 text-gray-500">
          User not found
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePhotosStore } from '@/stores/photos'
import AppHeader from '@/components/ui/AppHeader.vue'
import PhotoGrid from '@/components/photos/PhotoGrid.vue'
import apiClient from '@/api/client'
import type { User } from '@/types/user'

const route = useRoute()
const photosStore = usePhotosStore()

const user = ref<User | null>(null)
const loading = ref(true)

const userId = route.params.id as string

onMounted(async () => {
  try {
    // Fetch user profile
    const response = await apiClient.get(`/auth/users/${userId}`)
    user.value = response.data
    
    // Fetch user's public photos
    photosStore.fetchFeed(1, 20, userId)
  } catch {
    user.value = null
  } finally {
    loading.value = false
  }
})

const loadMore = () => {
  if (!photosStore.loading && photosStore.hasMorePhotos) {
    photosStore.fetchFeed(photosStore.currentPage + 1, 20, userId)
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
