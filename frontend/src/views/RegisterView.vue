<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
        Create your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Or
        <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
          sign in to existing account
        </router-link>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form v-if="!registered" class="space-y-6" @submit.prevent="handleRegister">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <div class="mt-1">
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="input-field"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="form.password"
                type="password"
                required
                minlength="8"
                class="input-field"
              />
            </div>
            <p class="mt-1 text-sm text-gray-500">Must be at least 8 characters</p>
          </div>

          <div>
            <label for="confirm-password" class="block text-sm font-medium text-gray-700">
              Confirm password
            </label>
            <div class="mt-1">
              <input
                id="confirm-password"
                v-model="form.confirmPassword"
                type="password"
                required
                class="input-field"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.loading || form.password !== form.confirmPassword"
              class="btn-primary w-full"
            >
              <span v-if="authStore.loading">Creating account...</span>
              <span v-else>Create account</span>
            </button>
          </div>
        </form>

        <div v-else class="text-center py-4">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
            <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-medium text-gray-900">Registration successful!</h3>
          <p class="mt-2 text-sm text-gray-500">
            Please check your email to verify your account before signing in.
          </p>
          <router-link to="/login" class="mt-4 inline-block btn-primary">
            Go to Sign In
          </router-link>
        </div>

        <div v-if="authStore.error" class="mt-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
          {{ authStore.error }}
        </div>

        <div v-if="form.password !== form.confirmPassword && form.confirmPassword" class="mt-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
          Passwords do not match
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const registered = ref(false)

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    return
  }
  
  try {
    await authStore.register({
      email: form.email,
      password: form.password,
    })
    registered.value = true
  } catch {
    // Error is handled by store
  }
}
</script>
