<template>
  <div class="relative min-h-screen md:flex">
    <!-- Mobile Menu -->
    <div class="bg-paper-sidebar text-gray-100 flex justify-between md:hidden">
      <router-link to="/" class="block p-4 text-white font-bold">Capacitações EAD</router-link>
      <button @click="sidebarOpen = !sidebarOpen" class="p-4 focus:outline-none focus:bg-paper-active-link">
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <!-- Sidebar -->
    <aside :class="{ '-translate-x-full': !sidebarOpen }" class="bg-paper-sidebar text-gray-100 w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform md:relative md:translate-x-0 transition duration-200 ease-in-out z-20">
      <div @click="() => router.push('/')" class="cursor-pointer text-white flex items-center space-x-2 px-4">
        <CubeTransparentIcon class="h-8 w-8"/>
        <span class="text-2xl font-extrabold">Capacitações EAD</span>
      </div>
      <div class="px-4 my-6">
        <div class="border-t border-white border-opacity-20"></div>
      </div>

      <nav>
        <router-link to="/" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
          <HomeIcon class="h-6 w-6"/>
          <span>Home</span>
        </router-link>

        <router-link v-if="authStore.isAuthenticated" to="/meus-cursos" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
          <AcademicCapIcon class="h-6 w-6" />
          <span>Meus Cursos</span>
        </router-link>

                      <router-link v-if="authStore.isManagerOrAdmin" to="/gestao-cursos" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
                        <ClipboardDocumentListIcon class="h-6 w-6" />
                        <span>Gestão de Cursos</span>
                      </router-link>
              
                      <router-link v-if="authStore.isManagerOrAdmin" to="/validacao-certificados" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
                        <ShieldCheckIcon class="h-6 w-6" />
                        <span>Validar Certificados</span>
                      </router-link>
        
                      <router-link v-if="authStore.isUdp" to="/gestao-usuarios" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
                        <UserGroupIcon class="h-6 w-6" />
                        <span>Gestão de Usuários</span>
                      </router-link>
        <!-- Novos links para Relatórios -->
        <div class="px-4 my-6">
          <div class="border-t border-white border-opacity-20"></div>
          <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider mt-4 block">Relatórios</span>
        </div>
        <router-link v-if="authStore.isUdp" to="/relatorios/udp" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
          <ChartBarIcon class="h-6 w-6" />
          <span>Relatórios UDP</span>
        </router-link>

        <router-link v-if="authStore.isManagerOrAdmin" to="/relatorios/chefia" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
          <ChartBarIcon class="h-6 w-6" />
          <span>Relatórios Chefia</span>
        </router-link>
      </nav>
    </aside>

    <!-- Content -->
    <div class="flex-1 flex flex-col bg-paper-bg z-10">
      <header class="flex justify-between items-center p-6 bg-transparent border-b border-gray-300">
        <div>
          <h1 class="text-2xl font-semibold text-paper-text">{{ $route.name }}</h1>
        </div>
        <div>
          <router-link v-if="!authStore.isAuthenticated" to="/login">
            <Button variant="primary">
              <template #icon>
                <ArrowRightOnRectangleIcon class="h-5 w-5" />
              </template>
              Login
            </Button>
          </router-link>
          <ProfileDropdown v-else />
        </div>
      </header>
      <main class="flex-1">
        <div class="container mx-auto px-4 py-4 md:py-6">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  HomeIcon,
  CubeTransparentIcon,
  Bars3Icon,
  ArrowRightOnRectangleIcon,
          AcademicCapIcon,
          ClipboardDocumentListIcon,
          UserGroupIcon,
          ChartBarIcon,
          ShieldCheckIcon,
        } from '@heroicons/vue/24/outline';
        import ProfileDropdown from '../components/ProfileDropdown.vue';
        import Button from '../components/Button.vue';
        import { useAuthStore } from '../stores/auth';
const sidebarOpen = ref(false);
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// Close sidebar on route change
watch(() => route.path, () => {
  sidebarOpen.value = false;
});
</script>
