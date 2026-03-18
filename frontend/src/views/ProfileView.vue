<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    
    <main class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">My Profile</h1>
          <p class="mt-2 text-gray-600">{{ authStore.user?.email }}</p>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Sidebar -->
          <div class="lg:col-span-1">
            <div class="card p-6">
              <div class="flex items-center space-x-4">
                <div class="h-16 w-16 rounded-full bg-primary-100 flex items-center justify-center">
                  <span class="text-2xl font-bold text-primary-700">
                    {{ authStore.user?.email[0].toUpperCase() }}
                  </span>
                </div>
                <div>
                  <h2 class="text-lg font-semibold text-gray-900">{{ authStore.user?.email }}</h2>
                  <p class="text-sm text-gray-500">Member since {{ formatDate(authStore.user?.created_at || '') }}</p>
                </div>
              </div>
              
              <div class="mt-6 border-t border-gray-200 pt-6">
                <div class="grid grid-cols-1 gap-4 text-center">
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="text-3xl font-bold text-primary-600">{{ photosStore.totalPhotos }}</div>
                    <div class="text-sm text-gray-500">Photos</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Photos grid -->
          <div class="lg:col-span-2">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900">My Photos</h2>
              <router-link to="/upload" class="btn-primary">Upload New</router-link>
            </div>
            
            <PhotoGrid
              :photos="photosStore.photos"
              :loading="photosStore.loading"
              @load-more="loadMore"
            />
            
            <div v-if="photosStore.photos.length === 0 && !photosStore.loading" class="text-center py-12 text-gray-500">
              You haven't uploaded any photos yet.
              <router-link to="/upload" class="text-primary-600 hover:text-primary-500 ml-1">Upload your first photo</router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePhotosStore } from '@/stores/photos'
import AppHeader from '@/components/ui/AppHeader.vue'
import PhotoGrid from '@/components/photos/PhotoGrid.vue'

const authStore = useAuthStore()
const photosStore = usePhotosStore()

onMounted(() => {
  photosStore.fetchMyPhotos(1)
})

const loadMore = () => {
  if (!photosStore.loading && photosStore.hasMorePhotos) {
    photosStore.fetchMyPhotos(photosStore.currentPage + 1)
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
