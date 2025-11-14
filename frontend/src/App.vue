<template>
  <div v-if="isAuthInitialized">
    <component :is="layout">
      <router-view />
    </component>
  </div>

</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
const route = useRoute();
const router = useRouter();
import { onMounted, computed, watch, ref } from 'vue';
import { useAuthStore } from './stores/auth';
import DefaultLayout from './layouts/DefaultLayout.vue';
import LoginLayout from './layouts/LoginLayout.vue';

const layout = computed(() => {
  return route.meta.layout === 'LoginLayout' ? LoginLayout : DefaultLayout;
});

const authStore = useAuthStore();
const isAuthInitialized = ref(false);

onMounted(async () => {
  console.log('🚀 App.vue - Iniciando auth...');
  await authStore.initializeAuth();
  isAuthInitialized.value = true;
  console.log('✅ App.vue - Auth inicializada');
});

// Watch for changes in authentication state and redirect to login if logged out
watch(() => authStore.isAuthenticated, (newIsAuthenticated, oldIsAuthenticated) => {
  console.log('👁️ Auth mudou:', { old: oldIsAuthenticated, new: newIsAuthenticated, route: route.name });
  if (oldIsAuthenticated && !newIsAuthenticated && route.name !== 'Login') {
    console.log('🔄 Redirecionando para login via router.push');
    router.push({ name: 'Login' });
  }
});</script>
