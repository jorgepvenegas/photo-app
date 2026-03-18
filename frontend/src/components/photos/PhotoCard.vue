<template>
  <div class="card hover:shadow-lg transition-shadow duration-200">
    <router-link :to="`/photos/${photo.id}`" class="block">
      <div class="aspect-square overflow-hidden bg-gray-100">
        <img
          :src="photo.thumb_medium_url || photo.storage_url"
          :alt="photo.title"
          class="w-full h-full object-cover hover:scale-105 transition-transform duration-200"
          loading="lazy"
        />
      </div>
    </router-link>
    
    <div class="p-4">
      <router-link :to="`/photos/${photo.id}`">
        <h3 class="text-lg font-semibold text-gray-900 truncate hover:text-primary-600">
          {{ photo.title }}
        </h3>
      </router-link>
      
      <p class="mt-1 text-sm text-gray-500">
        {{ formatDate(photo.created_at) }}
      </p>
      
      <div class="mt-3 flex items-center justify-between">
        <span
          v-if="!photo.is_public"
          class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800"
        >
          Private
        </span>
        
        <span v-else class="text-xs text-gray-400">
          Public
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Photo } from '@/types/photo'

defineProps<{
  photo: Photo
}>()

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}
</script>
