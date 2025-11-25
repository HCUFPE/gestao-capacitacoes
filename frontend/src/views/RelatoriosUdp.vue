<template>
  <div class="space-y-8">
    <PageHeader title="Relatórios UDP" />

    <!-- Relatório 1: Status Geral das Capacitações -->
    <Card variant="primary">
      <template #header>
        <h2 class="text-xl font-semibold">Status Geral das Capacitações</h2>
      </template>
      <div v-if="loading" class="text-center">Carregando...</div>
      <div v-else-if="error" class="text-red-500">Erro ao carregar dados.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
        <StatCard v-for="stat in statusGeral" :key="stat.name" :item="stat" />
      </div>
    </Card>

    <!-- Relatório 2: Cursos Mais Populares -->
    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Top 10 Cursos Mais Populares</h2>
      </template>
      <DataTable :headers="cursosPopularesHeaders" :items="cursosPopulares" :loading="loading" :error="error">
        <template #item-titulo="{ item }">
          <span class="font-medium">{{ item.titulo }}</span>
        </template>
      </DataTable>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import StatCard from '../components/StatCard.vue';
import DataTable from '../components/DataTable.vue';
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

// --- Status Geral ---
const rawStatusGeral = ref<Array<{ name: string; value: number }>>([]);
const statusGeral = computed(() => {
  const iconMap: { [key: string]: any } = {
    pendente: { icon: ClockIcon, color: 'text-yellow-500' },
    'em andamento': { icon: PlayIcon, color: 'text-blue-500' },
    realizado: { icon: CheckCircleIcon, color: 'text-cyan-500' },
    validado: { icon: ShieldCheckIcon, color: 'text-green-500' },
    recusado: { icon: XCircleIcon, color: 'text-red-500' },
  };
  return rawStatusGeral.value.map(stat => ({
    ...stat,
    name: stat.name.charAt(0).toUpperCase() + stat.name.slice(1), // Capitalize
    ...iconMap[stat.name.toLowerCase()],
  }));
});

const fetchStatusGeral = async () => {
  try {
    const { data } = await api.get('/api/relatorios/udp/status-geral');
    rawStatusGeral.value = data;
  } catch (err: any) {
    error.value = err;
    toast.error(`Erro ao carregar status geral: ${err.response?.data?.detail || err.message}`);
  }
};

// --- Cursos Populares ---
const cursosPopulares = ref<any[]>([]);
const cursosPopularesHeaders = [
  { text: 'Título do Curso', value: 'titulo' },
  { text: 'Total de Inscrições', value: 'total_inscricoes' },
  { text: 'Total de Atribuições', value: 'total_atribuicoes' },
];

const fetchCursosPopulares = async () => {
  try {
    const { data } = await api.get('/api/relatorios/udp/cursos-populares');
    cursosPopulares.value = data;
  } catch (err: any) {
    error.value = err;
    toast.error(`Erro ao carregar cursos populares: ${err.response?.data?.detail || err.message}`);
  }
};

onMounted(async () => {
  loading.value = true;
  await Promise.all([
    fetchStatusGeral(),
    fetchCursosPopulares(),
  ]);
  loading.value = false;
});
</script>
