<template>
  <div class="space-y-8">
    <PageHeader title="Relatórios UDP">
      <template #actions>
        <router-link :to="{ name: 'Relatórios Capacitações' }">
          <Button variant="primary" class="inline-flex items-center">
            <span class="mr-2">Ver Relatório Detalhado</span>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
            </svg>
          </Button>
        </router-link>
      </template>
    </PageHeader>

    <!-- Row 1: Status Geral (Cards + Gráfico) -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- KPIs -->
      <div class="xl:col-span-2">
        <Card variant="primary" class="h-full">
          <template #header>
            <h2 class="text-xl font-semibold">Status Geral (KPIs)</h2>
          </template>
          <div v-if="loading" class="text-center">Carregando...</div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <StatCard v-for="stat in statusGeral" :key="stat.name" :item="stat" />
          </div>
        </Card>
      </div>

      <!-- Gráfico Donut -->
      <Card class="h-full">
        <template #header>
          <h2 class="text-xl font-semibold">Distribuição</h2>
        </template>
        <div class="h-64 flex items-center justify-center p-4">
          <Doughnut v-if="!loading && statusChartData" :data="statusChartData" :options="doughnutOptions" />
          <div v-else-if="!loading" class="text-gray-500">Sem dados para exibir</div>
        </div>
      </Card>
    </div>

    <!-- Row 2: Conformidade por Setor (Gráfico de Barras) -->
    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Conformidade por Setor (%)</h2>
      </template>
      <div class="h-96 p-4">
        <Bar v-if="!loading && conformityChartData" :data="conformityChartData" :options="barOptions" />
      </div>
    </Card>

    <!-- Row 3: Cursos Mais Populares -->
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
import Button from '../components/Button.vue';
import { useToast } from 'vue-toastification';
import {
  ClockIcon,
  PlayIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  XCircleIcon,
} from '@heroicons/vue/24/outline';

// Chart.js Imports
import { Chart, registerables } from 'chart.js';
import { Bar, Doughnut } from 'vue-chartjs';

Chart.register(...registerables);

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();

// --- Data State ---
const rawStatusGeral = ref<Array<{ name: string; value: number }>>([]);
const conformidadeSetor = ref<any[]>([]);
const cursosPopulares = ref<any[]>([]);

// --- Computed for StatCards ---
const statusGeral = computed(() => {
  const iconMap: { [key: string]: any } = {
    pendente: { icon: ClockIcon, color: 'text-yellow-500' },
    'em andamento': { icon: PlayIcon, color: 'text-blue-500' },
    realizado: { icon: CheckCircleIcon, color: 'text-cyan-500' },
    validado: { icon: ShieldCheckIcon, color: 'text-green-500' },
    concluído: { icon: CheckCircleIcon, color: 'text-green-500' },
    recusado: { icon: XCircleIcon, color: 'text-red-500' },
  };
  return rawStatusGeral.value.map(stat => ({
    ...stat,
    name: stat.name.charAt(0).toUpperCase() + stat.name.slice(1), // Capitalize
    ...iconMap[stat.name.toLowerCase()] || { icon: ClockIcon, color: 'text-gray-500' },
  }));
});

// --- Chart Options ---
const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' as const },
  },
};

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y' as const, // Horizontal Bar Chart
  scales: {
    x: {
      beginAtZero: true,
      max: 100,
      title: { display: true, text: '% Conclusão' }
    }
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context: any) => `${context.raw.toFixed(1)}%`
      }
    }
  }
};

// --- Chart Data Computed ---
const statusChartData = computed(() => {
  if (!rawStatusGeral.value.length) return null;
  
  const labels = rawStatusGeral.value.map(s => s.name);
  const data = rawStatusGeral.value.map(s => s.value);
  const backgroundColor = rawStatusGeral.value.map(s => {
    const n = s.name.toLowerCase();
    if (n.includes('pendente')) return '#fbbf24'; // yellow-400
    if (n.includes('andamento')) return '#60a5fa'; // blue-400
    if (n.includes('realizado')) return '#22d3ee'; // cyan-400
    if (n.includes('validado')) return '#4ade80'; // green-400
    if (n.includes('concluído')) return '#4ade80'; // green-400
    if (n.includes('recusado')) return '#f87171'; // red-400
    return '#9ca3af';
  });

  return {
    labels,
    datasets: [{ data, backgroundColor, borderWidth: 0 }]
  };
});

const conformityChartData = computed(() => {
  if (!conformidadeSetor.value.length) return null;

  // Sort by progress descending and take top 15
  const sorted = [...conformidadeSetor.value]
    .map(s => ({
      label: s.lotacao,
      total: s['Total Atribuições'],
      completed: (s['Realizado'] || 0) + (s['Validado'] || 0) + (s['Concluído'] || 0), // Handle all completion statuses
      progress: s['Total Atribuições'] > 0 
        ? (((s['Realizado'] || 0) + (s['Validado'] || 0) + (s['Concluído'] || 0)) / s['Total Atribuições'] * 100) 
        : 0
    }))
    .sort((a, b) => b.progress - a.progress)
    .slice(0, 15); // Show top 15 sectors

  return {
    labels: sorted.map(s => s.label),
    datasets: [{
      label: 'Taxa de Conclusão (%)',
      data: sorted.map(s => s.progress),
      backgroundColor: '#3b82f6', // blue-500
      borderRadius: 4,
      barThickness: 20,
    }]
  };
});

// --- Headers for DataTable ---
const cursosPopularesHeaders = [
  { text: 'Título do Curso', value: 'titulo' },
  { text: 'Total de Inscrições', value: 'total_inscricoes' },
  { text: 'Total de Atribuições', value: 'total_atribuicoes' },
];

// --- Fetch Functions ---
const fetchData = async () => {
  try {
    const [statusRes, conformidadeRes, cursosRes] = await Promise.all([
      api.get('/api/relatorios/udp/status-geral'),
      api.get('/api/relatorios/udp/conformidade-lotacao'),
      api.get('/api/relatorios/udp/cursos-populares')
    ]);
    
    rawStatusGeral.value = statusRes.data;
    conformidadeSetor.value = conformidadeRes.data;
    cursosPopulares.value = cursosRes.data;
  } catch (err: any) {
    error.value = err;
    toast.error(`Erro ao carregar dados: ${err.response?.data?.detail || err.message}`);
  }
};

onMounted(async () => {
  loading.value = true;
  await fetchData();
  loading.value = false;
});
</script>