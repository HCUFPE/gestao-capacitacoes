<template>
  <div class="space-y-8">
    <PageHeader title="Relatórios da Chefia" />

    <!-- Relatório 1: Status de Cursos da Minha Lotação -->
    <Card variant="primary">
      <template #header>
        <h2 class="text-xl font-semibold">Status de Cursos da Minha Lotação</h2>
      </template>
      <div v-if="loading" class="text-center">Carregando...</div>
      <div v-else-if="error" class="text-red-500">Erro ao carregar dados.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
        <!-- Placeholder para StatCards -->
        <StatCard :item="{ name: 'Pendente', value: 0, icon: ClockIcon, color: 'text-yellow-500' }" />
        <StatCard :item="{ name: 'Em Andamento', value: 0, icon: PlayIcon, color: 'text-blue-500' }" />
        <StatCard :item="{ name: 'Realizado', value: 0, icon: CheckCircleIcon, color: 'text-cyan-500' }" />
        <StatCard :item="{ name: 'Validado', value: 0, icon: ShieldCheckIcon, color: 'text-green-500' }" />
        <StatCard :item="{ name: 'Recusado', value: 0, icon: XCircleIcon, color: 'text-red-500' }" />
      </div>
    </Card>

    <!-- Outros relatórios... -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import StatCard from '../components/StatCard.vue';
import PageHeader from '../components/PageHeader.vue';
import { useToast } from 'vue-toastification';
import {
  ClockIcon,
  PlayIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  XCircleIcon,
} from '@heroicons/vue/24/outline';

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();

// Lógica para buscar dados dos relatórios da chefia será adicionada aqui

onMounted(async () => {
  loading.value = true;
  // Exemplo: await fetchStatusLotacao();
  loading.value = false;
});
</script>
