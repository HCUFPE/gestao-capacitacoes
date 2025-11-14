<template>
  <div>
    <!-- Hero Welcome Card -->
    <div class="p-6 md:p-8 rounded-lg bg-paper-primary text-white shadow-lg">
      <h1 class="text-3xl md:text-4xl font-bold">Bem-vindo(a), {{ authStore.user?.displayName || 'Usuário' }}!</h1>
      <p class="mt-2 text-lg text-indigo-100">
        Acompanhe o progresso das capacitações da sua equipe e as suas.
      </p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
      <StatCard v-for="stat in stats" :key="stat.name" :item="stat" />
    </div>

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
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

import Button from '../components/Button.vue';
import StatCard from '../components/StatCard.vue'; // We will create this component

import { 
  AcademicCapIcon,
  ClipboardDocumentListIcon,
  UsersIcon,
  CheckBadgeIcon,
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();

const rawStats = ref({
  total_cursos: 0,
  total_inscricoes: 0,
  total_certificados_validados: 0,
  total_usuarios: 0,
});

const stats = computed(() => [
  {
    name: 'Cursos Disponíveis',
    value: rawStats.value.total_cursos,
    icon: AcademicCapIcon,
    color: 'text-blue-500',
  },
  {
    name: 'Inscrições Realizadas',
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

onMounted(fetchStats);
</script>