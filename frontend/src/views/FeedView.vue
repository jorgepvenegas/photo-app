<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    
    <main class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Photo Feed</h1>
          <router-link to="/upload" class="btn-primary">
            Upload Photo
          </router-link>
        </div>
        
        <PhotoGrid
          :photos="photosStore.photos"
          :loading="photosStore.loading"
          @load-more="loadMore"
        />
        
        <div v-if="photosStore.error" class="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
          {{ photosStore.error }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { usePhotosStore } from '@/stores/photos'
import AppHeader from '@/components/ui/AppHeader.vue'
import PhotoGrid from '@/components/photos/PhotoGrid.vue'

const photosStore = usePhotosStore()

onMounted(() => {
  photosStore.fetchFeed(1)
})

const loadMore = () => {
  if (!photosStore.loading && photosStore.hasMorePhotos) {
    photosStore.fetchFeed(photosStore.currentPage + 1)
  }
}
</script>
