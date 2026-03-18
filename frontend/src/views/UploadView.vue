<template>
  <div class="min-h-screen bg-gray-50">
    <AppHeader />
    
    <main class="py-8">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">Upload Photo</h1>
        
        <div class="card p-6">
          <!-- File input -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select photo
            </label>
            <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-primary-500 transition-colors">
              <div class="space-y-1 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <div class="flex text-sm text-gray-600 justify-center">
                  <label for="file-upload" class="relative cursor-pointer rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                    <span>Upload a file</span>
                    <input id="file-upload" name="file-upload" type="file" class="sr-only" accept="image/*" @change="handleFileSelect">
                  </label>
                  <p class="pl-1">or drag and drop</p>
                </div>
                <p class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
              </div>
            </div>
          </div>
          
          <div v-if="fileError" class="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md">
            {{ fileError }}
          </div>

          <!-- Preview -->
          <div v-if="previewUrl" class="mb-6">
            <img :src="previewUrl" alt="Preview" class="max-h-64 rounded-lg" />
          </div>
          
          <!-- Form -->
          <form v-if="selectedFile" @submit.prevent="handleUpload" class="space-y-4">
            <div>
              <label for="title" class="block text-sm font-medium text-gray-700">Title *</label>
              <input id="title" v-model="form.title" type="text" required class="input-field mt-1" />
            </div>
            
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
              <textarea id="description" v-model="form.description" rows="3" class="input-field mt-1 resize-none"></textarea>
            </div>
            
            <div class="flex items-center">
              <input id="is-public" v-model="form.is_public" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <label for="is-public" class="ml-2 block text-sm text-gray-900">Make this photo public</label>
            </div>
            
            <div class="flex gap-4">
              <button type="submit" :disabled="photosStore.uploading || !form.title" class="btn-primary flex-1">
                <span v-if="photosStore.uploading">Uploading...</span>
                <span v-else>Upload Photo</span>
              </button>
              <button type="button" @click="reset" class="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
        
        <div v-if="photosStore.error" class="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
          {{ photosStore.error }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { usePhotosStore } from '@/stores/photos'
import AppHeader from '@/components/ui/AppHeader.vue'

const router = useRouter()
const photosStore = usePhotosStore()

const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)
const form = reactive({
  title: '',
  description: '',
  is_public: true,
})

const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const fileError = ref<string | null>(null)

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  fileError.value = null

  if (!file) return

  if (!ALLOWED_TYPES.includes(file.type)) {
    fileError.value = 'Invalid file type. Allowed: JPG, PNG, GIF, WEBP'
    input.value = ''
    return
  }

  if (file.size > MAX_FILE_SIZE) {
    fileError.value = `File too large (${(file.size / 1024 / 1024).toFixed(1)}MB). Max: 10MB`
    input.value = ''
    return
  }

  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
  form.title = file.name.replace(/\.[^/.]+$/, '')
}

const handleUpload = async () => {
  if (!selectedFile.value || !form.title) return
  
  try {
    const photo = await photosStore.uploadPhoto(selectedFile.value, {
      title: form.title,
      description: form.description,
      is_public: form.is_public,
    })
    
    router.push(`/photos/${photo.id}`)
  } catch {
    // Error handled by store
  }
}

const reset = () => {
  selectedFile.value = null
  previewUrl.value = null
  form.title = ''
  form.description = ''
  form.is_public = true
}
</script>
