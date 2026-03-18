import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { photosApi } from '@/api/photos'
import type { Photo, PhotoList, PhotoDetail, UploadRequest, UploadConfirmRequest } from '@/types/photo'

export const usePhotosStore = defineStore('photos', () => {
  // State
  const photos = ref<Photo[]>([])
  const currentPhoto = ref<PhotoDetail | null>(null)
  const totalPhotos = ref(0)
  const currentPage = ref(1)
  const loading = ref(false)
  const uploading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const hasMorePhotos = computed(() => {
    return photos.value.length < totalPhotos.value
  })

  // Actions
  const fetchFeed = async (page = 1, perPage = 20) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await photosApi.list(page, perPage)
      
      if (page === 1) {
        photos.value = response.photos
      } else {
        photos.value.push(...response.photos)
      }
      
      totalPhotos.value = response.total
      currentPage.value = page
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load photos'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchMyPhotos = async (page = 1, perPage = 20) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await photosApi.listMyPhotos(page, perPage)
      
      if (page === 1) {
        photos.value = response.photos
      } else {
        photos.value.push(...response.photos)
      }
      
      totalPhotos.value = response.total
      currentPage.value = page
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load photos'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchPhoto = async (id: string) => {
    loading.value = true
    error.value = null
    
    try {
      const photo = await photosApi.get(id)
      currentPhoto.value = photo
      return photo
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load photo'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updatePhoto = async (id: string, data: Partial<Photo>) => {
    try {
      const updated = await photosApi.update(id, data)
      if (currentPhoto.value && currentPhoto.value.id === id) {
        currentPhoto.value = { ...currentPhoto.value, ...updated }
      }
      return updated
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update photo'
      throw err
    }
  }

  const deletePhoto = async (id: string) => {
    try {
      await photosApi.delete(id)
      photos.value = photos.value.filter(p => p.id !== id)
      if (currentPhoto.value?.id === id) {
        currentPhoto.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete photo'
      throw err
    }
  }

  const uploadPhoto = async (
    file: File,
    metadata: { title: string; description?: string; is_public?: boolean }
  ) => {
    uploading.value = true
    error.value = null
    
    try {
      // 1. Get presigned URL
      const presigned = await photosApi.getPresignedUrl({
        filename: file.name,
        content_type: file.type,
        file_size: file.size,
      })

      // 2. Upload directly to R2
      const uploadResponse = await fetch(presigned.upload_url, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type,
        },
      })

      if (!uploadResponse.ok) {
        throw new Error('Upload failed')
      }

      // 3. Confirm upload with metadata
      // Create an image element to get dimensions
      const img = new Image()
      const dimensions = await new Promise<{ width: number; height: number }>((resolve, reject) => {
        img.onload = () => {
          resolve({ width: img.naturalWidth, height: img.naturalHeight })
        }
        img.onerror = reject
        img.src = URL.createObjectURL(file)
      })

      const photo = await photosApi.confirmUpload({
        storage_key: presigned.storage_key,
        title: metadata.title,
        description: metadata.description || null,
        width: dimensions.width,
        height: dimensions.height,
        file_size: file.size,
        mime_type: file.type,
        is_public: metadata.is_public ?? true,
      })

      // Add to list
      photos.value.unshift(photo)
      return photo
    } catch (err: any) {
      error.value = err.message || 'Upload failed'
      throw err
    } finally {
      uploading.value = false
    }
  }

  return {
    photos,
    currentPhoto,
    totalPhotos,
    currentPage,
    loading,
    uploading,
    error,
    hasMorePhotos,
    fetchFeed,
    fetchMyPhotos,
    fetchPhoto,
    updatePhoto,
    deletePhoto,
    uploadPhoto,
  }
})
