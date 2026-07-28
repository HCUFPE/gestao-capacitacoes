<template>
  <div class="space-y-8">
    <PageHeader title="Relatório Detalhado de Capacitações">
      <template #actions>
        <div class="flex space-x-4">
          <Button @click="downloadExcel" :loading="downloadingExcel" variant="secondary">
            Exportar Excel
          </Button>
          <Button @click="downloadPdf" :loading="downloadingPdf" variant="secondary">
            Exportar PDF
          </Button>
        </div>
      </template>
    </PageHeader>

    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Listagem Completa</h2>
      </template>
      
      <!-- Filtros -->
      <div class="flex space-x-4 items-center mb-4">
        <!-- Filter: Ano -->
        <select
          v-model="filterAno"
          @change="fetchData"
          class="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        >
          <option value="">Todos os anos</option>
          <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
        </select>

        <!-- Filter: Vínculo -->
        <select
          v-model="filterVinculo"
          @change="fetchData"
          class="px-3 py-2 bg-white border border-gray-300 rounded-md text-sm"
        >
          <option value="">Todos os vínculos</option>
          <option v-for="v in vinculosDisponiveis" :key="v" :value="v">{{ v }}</option>
        </select>
      </div>

      <DataTable 
        :headers="headers" 
        :items="items" 
        :loading="loading" 
        :error="error"
      >
        <template #nome_profissional="{ item }">
          <button
            @click="openUserDetails(item.id)"
            class="text-blue-500 hover:text-blue-700 font-medium"
          >
            {{ item.nome_profissional }}
          </button>
        </template>
        <template #item-certificado="{ item }">
          <span :class="item.certificado === 'Sim' ? 'text-green-600 font-bold' : 'text-gray-500'">
            {{ item.certificado }}
          </span>
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
import api from '../services/api';
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

const headers = [
  { text: 'Profissional', value: 'nome_profissional' },
  { text: 'CPF', value: 'cpf' },
  { text: 'Vínculo', value: 'vinculo' },
  { text: 'Setor', value: 'setor' },
  { text: 'Curso', value: 'nome_curso' },
  { text: 'Plataforma', value: 'plataforma' },
  { text: 'CH', value: 'carga_horaria' },
  { text: 'Ano GD', value: 'ano_gd' },
  { text: 'Certificado', value: 'certificado' },
];

const fetchData = async () => {
  try {
    loading.value = true;
    const params: Record<string, string> = {};
    if (filterAno.value) params.ano = filterAno.value;
    if (filterVinculo.value) params.vinculo = filterVinculo.value;
    const { data } = await api.get('/api/relatorios/capacitacoes', { params });
    items.value = data;
  } catch (err: any) {
    error.value = err;
    toast.error(`Erro ao carregar dados: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};

const downloadFile = async (url: string, filename: string, loadingRef: any) => {
  try {
    loadingRef.value = true;
    const params: Record<string, string> = {};
    if (filterAno.value) params.ano = filterAno.value;
    if (filterVinculo.value) params.vinculo = filterVinculo.value;
    const response = await api.get(url, { responseType: 'blob', params });
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(link.href);
    toast.success('Download iniciado!');
  } catch (err: any) {
    toast.error(`Erro no download: ${err.response?.data?.detail || err.message}`);
  } finally {
    loadingRef.value = false;
  }
};

const downloadExcel = () => downloadFile('/api/relatorios/capacitacoes/export/excel', 'relatorio_capacitacoes.xlsx', downloadingExcel);
const downloadPdf = () => downloadFile('/api/relatorios/capacitacoes/export/pdf', 'relatorio_capacitacoes.pdf', downloadingPdf);

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

const fetchVinculos = async () => {
  try {
    const { data } = await api.get('/api/relatorios/vinculos');
    vinculosDisponiveis.value = data;
  } catch {
    // Vinculos may not be available, ignore
  }
};

onMounted(async () => {
  await fetchVinculos();
  fetchData();
});
</script>
