<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    <PhotoCard
      v-for="photo in photos"
      :key="photo.id"
      :photo="photo"
    />
  </div>
  
  <div v-if="loading" class="text-center py-8">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
  </div>
  
  <div v-if="hasMore && !loading" class="text-center py-8">
    <button
      @click="$emit('load-more')"
      class="btn-secondary"
    >
      Load more
    </button>
  </div>
  
  <div v-if="!hasMore && photos.length > 0" class="text-center py-8 text-gray-500">
    No more photos
  </div>
</template>

<script setup lang="ts">
import PhotoCard from './PhotoCard.vue'
import type { Photo } from '@/types/photo'

defineProps<{
  photos: Photo[]
  loading?: boolean
  hasMore?: boolean
}>()

defineEmits<{
  (e: 'load-more'): void
}>()
</script>
