<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    
    <main class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
            Share Your Moments
          </h1>
          <p class="mt-4 text-xl text-gray-600">
            Upload, share, and discover amazing photos
          </p>
          
          <div class="mt-8 flex justify-center gap-4">
            <router-link
              v-if="!authStore.isAuthenticated"
              to="/register"
              class="btn-primary text-lg px-8 py-3"
            >
              Get Started
            </router-link>
            <router-link
              v-if="!authStore.isAuthenticated"
              to="/login"
              class="btn-secondary text-lg px-8 py-3"
            >
              Sign In
            </router-link>
            <router-link
              v-else
              to="/feed"
              class="btn-primary text-lg px-8 py-3"
            >
              View Feed
            </router-link>
          </div>
        </div>
        
        <!-- Sample photos grid (if we have any public photos) -->
        <div v-if="photosStore.photos.length > 0" class="mt-16">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Recent Photos</h2>
          <PhotoGrid :photos="photosStore.photos.slice(0, 6)" />
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
  // Load some public photos for the homepage
  photosStore.fetchFeed(1, 6).catch(() => {})
})
</script>
