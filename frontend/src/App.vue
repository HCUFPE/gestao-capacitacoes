<template>
  <div v-if="isAuthInitialized">
    <component :is="layout">
      <router-view />
    </component>
  </div>
  <LoadingIndicator />
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();

import { onMounted, computed, watch, ref } from 'vue';
import { useAuthStore } from './stores/auth';
import DefaultLayout from './layouts/DefaultLayout.vue';
import LoginLayout from './layouts/LoginLayout.vue';
import LoadingIndicator from './components/LoadingIndicator.vue';

const layout = computed(() => {
  return route.meta.layout === 'LoginLayout' ? LoginLayout : DefaultLayout;
});

const authStore = useAuthStore();
const isAuthInitialized = ref(false);

onMounted(async () => {
  await authStore.initializeAuth();
  isAuthInitialized.value = true;
});

// Watch for changes in authentication state and redirect to login if logged out
watch(() => authStore.isAuthenticated, (newIsAuthenticated, oldIsAuthenticated) => {
  if (oldIsAuthenticated && !newIsAuthenticated && route.name !== 'Login') {
    router.push({ name: 'Login' });
  }
});
</script>
