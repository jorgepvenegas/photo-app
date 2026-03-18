<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 text-center">
        <div v-if="verifying" class="py-4">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Verifying your email...</p>
        </div>
        
        <div v-else-if="success" class="py-4">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
            <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-medium text-gray-900">Email verified!</h3>
          <p class="mt-2 text-sm text-gray-500">
            Your email has been verified. You can now sign in to your account.
          </p>
          <router-link to="/login" class="mt-4 inline-block btn-primary">
            Sign In
          </router-link>
        </div>
        
        <div v-else class="py-4">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
            <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-medium text-gray-900">Verification failed</h3>
          <p class="mt-2 text-sm text-gray-500">
            {{ error || 'The verification link is invalid or has expired.' }}
          </p>
          <router-link to="/login" class="mt-4 inline-block btn-primary">
            Go to Sign In
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const verifying = ref(true)
const success = ref(false)
const error = ref('')

onMounted(async () => {
  const token = route.query.token as string
  
  if (!token) {
    verifying.value = false
    error.value = 'No verification token provided'
    return
  }
  
  try {
    await authStore.verifyEmail(token)
    success.value = true
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Verification failed'
  } finally {
    verifying.value = false
  }
})
</script>
