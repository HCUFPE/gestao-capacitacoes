<template>
  <div class="space-y-8">
    <PageHeader title="Relatórios da Chefia">
      <template #actions>
        <router-link :to="{ name: 'Relatório Consolidado Chefia' }">
          <Button variant="info" class="inline-flex items-center">
            <TableCellsIcon class="w-5 h-5 mr-2" />
            Relatório Consolidado
          </Button>
        </router-link>
      </template>
    </PageHeader>

    <!-- Row 1: Status da Equipe (KPIs + Gráfico) -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- KPIs -->
      <div class="xl:col-span-2">
        <Card variant="primary" class="h-full">
          <template #header>
            <h2 class="text-xl font-semibold">Status da Minha Equipe (Lotação)</h2>
          </template>
          <div v-if="loading" class="text-center">Carregando...</div>
          <div v-else-if="error" class="text-red-500">Erro ao carregar dados.</div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <StatCard v-for="stat in statusLotacao" :key="stat.name" :item="stat" />
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

    <!-- Row 2: Progresso Individual -->
    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Progresso Individual da Equipe</h2>
        <div class="flex space-x-4 items-center mt-2">
          <!-- Filter: Ano -->
          <select
            v-model="filterAno"
            @change="applyFilters"
            class="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
          >
            <option value="">Todos os anos</option>
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
          </select>

          <!-- Filter: Vínculo -->
          <select
            v-model="filterVinculo"
            @change="applyFilters"
            class="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
          >
            <option value="">Todos os vínculos</option>
            <option v-for="v in vinculosDisponiveis" :key="v" :value="v">{{ v }}</option>
          </select>
        </div>
      </template>
      <DataTable :headers="progressoHeaders" :items="progressoIndividual" :loading="loading" :error="error">
        <template #item-nome="{ item }">
          <button
            @click="openSubordinadoDetails(item.id)"
            class="text-blue-500 hover:text-blue-700 font-medium"
          >
            {{ item.nome }}
          </button>
        </template>
        <template #item-progresso="{ item }">
          <div class="flex items-center">
            <span class="mr-2 text-sm text-gray-700">{{ item.progresso }}%</span>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: item.progresso + '%' }"></div>
            </div>
          </div>
        </template>
      </DataTable>
    </Card>

    <!-- Subordinado Details Modal -->
    <Modal :show="isSubordinadoModalOpen" @close="closeSubordinadoModal" size="5xl">
      <template #header>
        <h2 class="text-xl font-semibold">Detalhes do Subordinado: {{ subordinadoNome }}</h2>
      </template>
      <div v-if="subordinadoLoading" class="text-center py-4">Carregando...</div>
      <div v-else>
        <DataTable :headers="subordinadoHeaders" :items="subordinadoCursos">
          <template #item-certificado="{ item }">
            <a
              v-if="item.certificado_file_path || item.certificado_link"
              :href="getCertificateUrl(item) ?? ''"
              target="_blank"
              class="text-blue-500 hover:text-blue-700"
            >
              Visualizar
            </a>
            <span v-else class="text-gray-400">—</span>
          </template>
        </DataTable>
      </div>
      <template #footer>
        <div class="flex justify-end">
          <Button @click="closeSubordinadoModal" variant="default">
            Fechar
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';
import { getCertificateUrl } from '../services/certificateUtils';
import Card from '../components/Card.vue';
import StatCard from '../components/StatCard.vue';
import DataTable from '../components/DataTable.vue';
import PageHeader from '../components/PageHeader.vue';
import Modal from '../components/Modal.vue';
import Button from '../components/Button.vue';
import { useToast } from 'vue-toastification';
import {
  ClockIcon,
  PlayIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  XCircleIcon,
  TableCellsIcon,
} from '@heroicons/vue/24/outline';

// Chart.js Imports
import { Chart, registerables } from 'chart.js';
import { Doughnut } from 'vue-chartjs';

Chart.register(...registerables);

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();

// --- Filters ---
const filterAno = ref('');
const filterVinculo = ref('');
const vinculosDisponiveis = ref<string[]>([]);

const availableYears = computed(() => {
  const currentYear = new Date().getFullYear();
  const years: string[] = [];
  for (let i = currentYear - 5; i <= currentYear + 1; i++) years.push(String(i));
  return years;
});

// --- Data ---
const rawStatusLotacao = ref<Array<{ name: string; value: number }>>([]);
const progressoIndividual = ref<any[]>([]);

// --- Subordinado Details ---
const isSubordinadoModalOpen = ref(false);
const subordinadoNome = ref('');
const subordinadoLoading = ref(false);
const subordinadoCursos = ref<any[]>([]);

const subordinadoHeaders = [
  { text: 'Curso', value: 'curso.titulo' },
  { text: 'Plataforma', value: 'curso.certificadora' },
  { text: 'CH', value: 'curso.carga_horaria' },
  { text: 'Ano GD', value: 'curso.ano_gd' },
  { text: 'Status', value: 'status' },
  { text: 'Certificado', value: 'certificado' },
];

// --- Status Lotacao Computed ---
const statusLotacao = computed(() => {
  const iconMap: { [key: string]: any } = {
    pendente: { icon: ClockIcon, color: 'text-yellow-500' },
    'em andamento': { icon: PlayIcon, color: 'text-blue-500' },
    realizado: { icon: CheckCircleIcon, color: 'text-cyan-500' },
    validado: { icon: ShieldCheckIcon, color: 'text-green-500' },
    concluído: { icon: CheckCircleIcon, color: 'text-green-500' },
    recusado: { icon: XCircleIcon, color: 'text-red-500' },
  };
  return rawStatusLotacao.value.map(stat => ({
    ...stat,
    name: stat.name.charAt(0).toUpperCase() + stat.name.slice(1),
    ...iconMap[stat.name.toLowerCase()] || { icon: ClockIcon, color: 'text-gray-500' },
  }));
});

// --- Chart Data ---
const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' as const },
  },
};

const statusChartData = computed(() => {
  if (!rawStatusLotacao.value.length) return null;
  
  const labels = rawStatusLotacao.value.map(s => s.name);
  const data = rawStatusLotacao.value.map(s => s.value);
  const backgroundColor = rawStatusLotacao.value.map(s => {
    const n = s.name.toLowerCase();
    if (n.includes('pendente')) return '#fbbf24';
    if (n.includes('andamento')) return '#60a5fa';
    if (n.includes('realizado')) return '#22d3ee';
    if (n.includes('validado')) return '#4ade80';
    if (n.includes('recusado')) return '#f87171';
    return '#9ca3af';
  });

  return {
    labels,
    datasets: [{ data, backgroundColor, borderWidth: 0 }]
  };
});

// --- Table Headers ---
const progressoHeaders = [
  { text: 'Nome', value: 'nome' },
  { text: 'Matrícula', value: 'matricula' },
  { text: 'Cargo', value: 'cargo' },
  { text: 'Vínculo', value: 'vinculo' },
  { text: 'Cursos Atribuídos', value: 'total_cursos' },
  { text: 'Concluídos', value: 'concluidos' },
  { text: 'Progresso', value: 'progresso' },
];

// --- Fetch Functions ---
const fetchData = async () => {
  try {
    const params: Record<string, string> = {};
    if (filterAno.value) params.ano = filterAno.value;
    if (filterVinculo.value) params.vinculo = filterVinculo.value;

    const [statusRes, progressoRes] = await Promise.all([
      api.get('/api/relatorios/chefia/status-lotacao', { params }),
      api.get('/api/relatorios/chefia/progresso-individual', { params })
    ]);
    
    rawStatusLotacao.value = statusRes.data;
    progressoIndividual.value = progressoRes.data;
  } catch (err: any) {
    // Se for 403 ou 404, pode ser que o usuário não tenha lotação ou perfil
    error.value = err;
    toast.error(`Erro ao carregar dados da chefia: ${err.response?.data?.detail || err.message}`);
  }
};

const applyFilters = () => {
  loading.value = true;
  fetchData().then(() => { loading.value = false; });
};

// --- Subordinado Details ---
const openSubordinadoDetails = async (subordinadoId: string) => {
  const subordinado = progressoIndividual.value.find(s => s.id === subordinadoId);
  if (!subordinado) return;

  subordinadoNome.value = subordinado.nome;
  subordinadoLoading.value = true;
  isSubordinadoModalOpen.value = true;
  subordinadoCursos.value = [];

  try {
    const { data } = await api.get(`/api/relatorios/chefia/subordinado/${subordinadoId}`);
    subordinadoCursos.value = data;
  } catch (err: any) {
    toast.error(`Erro ao carregar detalhes: ${err.response?.data?.detail || err.message}`);
  } finally {
    subordinadoLoading.value = false;
  }
};

const closeSubordinadoModal = () => {
  isSubordinadoModalOpen.value = false;
  subordinadoCursos.value = [];
  subordinadoNome.value = '';
};


const fetchVinculos = async () => {
  try {
    const { data } = await api.get('/api/relatorios/vinculos');
    vinculosDisponiveis.value = data;
  } catch {
    // Vinculos may not be available, ignore
  }
};

onMounted(async () => {
  loading.value = true;
  await fetchVinculos();
  await fetchData();
  loading.value = false;
});
</script>