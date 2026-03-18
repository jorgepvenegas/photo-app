import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('./views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('./views/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('./views/RegisterView.vue'),
      meta: { guest: true },
    },
    {
      path: '/verify-email',
      name: 'VerifyEmail',
      component: () => import('./views/VerifyEmailView.vue'),
    },
    {
      path: '/feed',
      name: 'Feed',
      component: () => import('./views/FeedView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/photos/:id',
      name: 'PhotoDetail',
      component: () => import('./views/PhotoDetailView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/upload',
      name: 'Upload',
      component: () => import('./views/UploadView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('./views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/users/:id',
      name: 'UserProfile',
      component: () => import('./views/UserProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('./views/NotFoundView.vue'),
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if user is authenticated
  if (!authStore.isAuthenticated && authStore.token) {
    try {
      await authStore.fetchUser()
    } catch {
      authStore.logout()
    }
  }
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/feed')
  } else {
    next()
  }
})

export default router
