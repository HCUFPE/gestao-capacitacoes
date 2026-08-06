<template>
  <div>
    <!-- Hero Welcome Card -->
    <div class="p-6 md:p-8 rounded-lg bg-paper-primary text-white shadow-lg">
      <h1 class="text-3xl md:text-4xl font-bold">Bem-vindo(a), {{ authStore.user?.displayName || 'Usuário' }}!</h1>
      <p class="mt-2 text-lg text-indigo-100">
        Acompanhe o progresso das capacitações da sua equipe e as suas.
      </p>
    </div>

    <!-- Personal Stats Grid -->
    <section class="mt-8">
      <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center space-x-2">
        <UserIcon class="h-6 w-6 text-indigo-600" />
        <span>Seu Panorama Pessoal</span>
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <StatCard v-for="stat in personalStats" :key="stat.name" :item="stat" />
      </div>
    </section>

    <!-- Global Stats Grid -->
    <section class="mt-8">
      <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center space-x-2">
        <GlobeAltIcon class="h-6 w-6 text-blue-600" />
        <span>Visão Geral do Sistema</span>
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard v-for="stat in globalStats" :key="stat.name" :item="stat" />
      </div>
    </section>

    <!-- Action Buttons -->
    <div class="mt-8 flex flex-col sm:flex-row gap-4">
      <router-link v-if="authStore.isAuthenticated" to="/meus-cursos" class="w-full sm:w-auto">
        <Button variant="primary" class="w-full justify-center">
          <template #icon><AcademicCapIcon class="h-5 w-5" /></template>
          Ver Meus Cursos
        </Button>
      </router-link>
      <router-link v-if="authStore.isManagerOrAdmin" to="/gestao-cursos" class="w-full sm:w-auto">
        <Button variant="secondary" class="w-full justify-center">
          <template #icon><ClipboardDocumentListIcon class="h-5 w-5" /></template>
          Gerenciar Cursos
        </Button>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

import Button from '../components/Button.vue';
import StatCard from '../components/StatCard.vue';

import { 
  AcademicCapIcon,
  ClipboardDocumentListIcon,
  UsersIcon,
  CheckBadgeIcon,
  UserIcon,
  GlobeAltIcon,
  ArrowUpTrayIcon,
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();

const rawStats = ref({
  total_cursos: 0,
  total_inscricoes: 0,
  total_certificados_validados: 0,
  total_usuarios: 0,
  minhas_inscricoes: 0,
  meus_certificados_enviados: 0,
  meus_certificados_validados: 0,
});

const personalStats = computed(() => [
  {
    name: 'Minhas Inscrições',
    value: rawStats.value.minhas_inscricoes,
    icon: AcademicCapIcon,
    color: 'text-indigo-600',
  },
  {
    name: 'Certificados Enviados',
    value: rawStats.value.meus_certificados_enviados,
    icon: ArrowUpTrayIcon,
    color: 'text-blue-500',
  },
  {
    name: 'Certificados Validados',
    value: rawStats.value.meus_certificados_validados,
    icon: CheckBadgeIcon,
    color: 'text-green-600',
  },
]);

const globalStats = computed(() => [
  {
    name: 'Cursos Disponíveis',
    value: rawStats.value.total_cursos,
    icon: AcademicCapIcon,
    color: 'text-blue-500',
  },
  {
    name: 'Inscrições no Sistema',
    value: rawStats.value.total_inscricoes,
    icon: ClipboardDocumentListIcon,
    color: 'text-indigo-500',
  },
  {
    name: 'Certificados Validados',
    value: rawStats.value.total_certificados_validados,
    icon: CheckBadgeIcon,
    color: 'text-green-500',
  },
  {
    name: 'Usuários na Plataforma',
    value: rawStats.value.total_usuarios,
    icon: UsersIcon,
    color: 'text-yellow-500',
  },
]);

const fetchStats = async () => {
  try {
    const { data } = await api.get('/api/utils/stats');
    rawStats.value = data;
  } catch (error) {
    console.error("Falha ao carregar estatísticas:", error);
  }
};

// Polling de 30s inteligente com pausa quando a aba estiver em segundo plano
const POLL_INTERVAL = 30000;
let timer: ReturnType<typeof setInterval> | null = null;

const startPolling = () => {
  if (timer) clearInterval(timer);
  timer = setInterval(() => {
    if (!document.hidden) {
      fetchStats();
    }
  }, POLL_INTERVAL);
};

const stopPolling = () => {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
};

const handleVisibilityChange = () => {
  if (document.hidden) {
    stopPolling();
  } else {
    fetchStats();
    startPolling();
  }
};

onMounted(() => {
  fetchStats();
  startPolling();
  document.addEventListener('visibilitychange', handleVisibilityChange);
});

onUnmounted(() => {
  stopPolling();
  document.removeEventListener('visibilitychange', handleVisibilityChange);
});
</script>