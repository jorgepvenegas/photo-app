<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <!-- Logo -->
        <router-link to="/" class="flex items-center">
          <h1 class="text-xl font-bold text-primary-600">PhotoApp</h1>
        </router-link>
        
        <!-- Navigation -->
        <nav class="flex items-center gap-4">
          <template v-if="authStore.isAuthenticated">
            <router-link to="/feed" class="text-gray-600 hover:text-gray-900">
              Feed
            </router-link>
            <router-link to="/upload" class="text-gray-600 hover:text-gray-900">
              Upload
            </router-link>
            <router-link to="/profile" class="text-gray-600 hover:text-gray-900">
              Profile
            </router-link>
            <button
              @click="handleLogout"
              class="text-gray-600 hover:text-gray-900"
            >
              Logout
            </button>
          </template>
          
          <template v-else>
            <router-link to="/login" class="text-gray-600 hover:text-gray-900">
              Sign In
            </router-link>
            <router-link to="/register" class="btn-primary">
              Sign Up
            </router-link>
          </template>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
