<template>
  <div class="space-y-8">
    <PageHeader :title="title">
      <template #actions>
        <Button @click="downloadExcel" :loading="downloadingExcel" variant="primary" class="inline-flex items-center mr-2">
          <span class="mr-2">Exportar Excel</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
        </Button>
        <Button @click="downloadPdf" :loading="downloadingPdf" variant="secondary" class="inline-flex items-center">
          <span class="mr-2">Exportar PDF</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
        </Button>
      </template>
    </PageHeader>

    <!-- Filtros -->
    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Filtros</h2>
      </template>
      <div class="flex space-x-4 items-center">
        <select
          v-model="filterAno"
          @change="fetchData"
          class="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        >
          <option value="">Todos os anos</option>
          <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
        </select>

        <select
          v-model="filterVinculo"
          @change="fetchData"
          class="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        >
          <option value="">Todos os vínculos</option>
          <option v-for="v in vinculosDisponiveis" :key="v" :value="v">{{ v }}</option>
        </select>

        <button
          @click="clearFilters"
          class="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 underline"
        >
          Limpar filtros
        </button>
      </div>
    </Card>

    <!-- Tabela Consolidada -->
    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Relatório Consolidado ({{ items.length }} registros)</h2>
      </template>
      <DataTable :headers="headers" :items="items" :loading="loading" :error="error">
        <template #nome="{ item }">
          <button
            @click="openUserDetails(item.id)"
            class="text-blue-500 hover:text-blue-700 font-medium"
          >
            {{ item.nome }}
          </button>
        </template>
        <template #item-status="{ item }">
          <span :class="getStatusClass(item.status)" class="px-2 py-1 rounded-full text-xs bg-gray-50 border border-gray-100">{{ item.status }}</span>
        </template>
        <template #item-certificado_enviado="{ item }">
          <div v-if="item.certificado_enviado === 'Sim'" class="flex items-center text-green-600 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 mr-1">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
            Sim
          </div>
          <div v-else class="flex items-center text-red-500 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 mr-1">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Não
          </div>
        </template>
        <template #item-certificado_link="{ item }">
          <a
            v-if="item.certificado_file_path || item.certificado_link"
            :href="getCertificateUrl(item) ?? ''"
            target="_blank"
            class="text-green-600 hover:text-green-800 flex items-center justify-center"
            title="Visualizar Certificado"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </a>
          <div v-else class="text-red-400 flex items-center justify-center" title="Pendente">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </template>
        <template #item-validacao="{ item }">
          <div v-if="item.status === 'Validado'" class="flex items-center justify-center text-green-600" title="Validado">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div v-else-if="item.status === 'Inválido' || item.status === 'Rejeitado'" class="flex items-center justify-center text-red-500" title="Inválido">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div v-else-if="item.certificado_enviado === 'Sim'" class="flex items-center justify-center text-yellow-500" title="Aguardando Validação">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div v-else class="text-gray-400 flex items-center justify-center" title="Sem Certificado">-</div>
        </template>
      </DataTable>
    </Card>

    <!-- User Details Modal -->
    <UserDetailsModal
      :show="isUserModalOpen"
      :userId="selectedUserId"
      @close="closeUserModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import api from '../services/api';
import { getCertificateUrl } from '../services/certificateUtils';
import Card from '../components/Card.vue';
import DataTable from '../components/DataTable.vue';
import PageHeader from '../components/PageHeader.vue';
import Button from '../components/Button.vue';
import UserDetailsModal from '../components/UserDetailsModal.vue';
import { useToast } from 'vue-toastification';

const loading = ref(true);
const downloadingExcel = ref(false);
const downloadingPdf = ref(false);
const error = ref<Error | null>(null);
const items = ref<any[]>([]);
const toast = useToast();
const route = useRoute();

const isChefia = computed(() => route.meta.role === 'CHEFIA');

const title = computed(() => {
  return isChefia.value ? 'Relatório Consolidado - Minha Equipe' : 'Relatório Consolidado - Todas as Equipes';
});

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

// --- Table Headers ---
const headers = [
  { text: 'Nome', value: 'nome' },
  { text: 'Vínculo', value: 'vinculo' },
  { text: 'Setor', value: 'setor' },
  { text: 'Curso', value: 'nome_curso' },
  { text: 'Plataforma', value: 'certificadora' },
  { text: 'CH', value: 'carga_horaria' },
  { text: 'Ano GD', value: 'ano_gd' },
  { text: 'Status', value: 'status' },
  { text: 'Envio Certificado', value: 'data_envio_certificado' },
  { text: 'Certificado Enviado', value: 'certificado_enviado' },
  { text: 'Certificado', value: 'certificado_link' },
  { text: 'Validação', value: 'validacao' },
];

// --- Helpers ---
const getStatusClass = (status: string) => {
  switch (status) {
    case 'Realizado':
    case 'Concluído':
    case 'Validado':
      return 'text-green-600 font-semibold';
    case 'Em Andamento':
      return 'text-blue-600 font-semibold';
    case 'Pendente':
      return 'text-yellow-600 font-semibold';
    default:
      return 'text-gray-500';
  }
};


// --- Fetch Functions ---
const fetchData = async () => {
  try {
    loading.value = true;
    const params: Record<string, string> = {};
    if (filterAno.value) params.ano = filterAno.value;
    if (filterVinculo.value) params.vinculo = filterVinculo.value;

    const endpoint = isChefia.value
      ? '/api/relatorios/chefia/consolidado'
      : '/api/relatorios/udp/consolidado';

    const { data } = await api.get(endpoint, { params });
    items.value = data;
  } catch (err: any) {
    error.value = err;
    toast.error(`Erro ao carregar dados: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};

const downloadExcel = async () => {
  try {
    downloadingExcel.value = true;
    const params: Record<string, string> = {};
    if (filterAno.value) params.ano = filterAno.value;
    if (filterVinculo.value) params.vinculo = filterVinculo.value;

    const endpoint = isChefia.value
      ? '/api/relatorios/chefia/consolidado/export/excel'
      : '/api/relatorios/udp/consolidado/export/excel';

    const response = await api.get(endpoint, { responseType: 'blob', params });
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'relatorio_consolidado.xlsx';
    link.click();
    window.URL.revokeObjectURL(link.href);
    toast.success('Download iniciado!');
  } catch (err: any) {
    toast.error(`Erro no download: ${err.response?.data?.detail || err.message}`);
  } finally {
    downloadingExcel.value = false;
  }
};

const downloadPdf = async () => {
  try {
    downloadingPdf.value = true;
    const params: Record<string, string> = {};
    if (filterAno.value) params.ano = filterAno.value;
    if (filterVinculo.value) params.vinculo = filterVinculo.value;

    const endpoint = isChefia.value
      ? '/api/relatorios/chefia/consolidado/export/pdf'
      : '/api/relatorios/udp/consolidado/export/pdf';

    const response = await api.get(endpoint, { responseType: 'blob', params });
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'relatorio_consolidado.pdf';
    link.click();
    window.URL.revokeObjectURL(link.href);
    toast.success('Download iniciado!');
  } catch (err: any) {
    toast.error(`Erro no download: ${err.response?.data?.detail || err.message}`);
  } finally {
    downloadingPdf.value = false;
  }
};

const fetchVinculos = async () => {
  try {
    const { data } = await api.get('/api/relatorios/vinculos');
    vinculosDisponiveis.value = data;
  } catch {
    // Vinculos may not be available, ignore
  }
};

const clearFilters = () => {
  filterAno.value = '';
  filterVinculo.value = '';
  fetchData();
};

// --- User Details Modal ---
const isUserModalOpen = ref(false);
const selectedUserId = ref('');

const openUserDetails = (userId: string) => {
  if (!userId) return;
  selectedUserId.value = userId;
  isUserModalOpen.value = true;
};

const closeUserModal = () => {
  isUserModalOpen.value = false;
  selectedUserId.value = '';
};

onMounted(async () => {
  await fetchVinculos();
  await fetchData();
  loading.value = false;
});
</script>
