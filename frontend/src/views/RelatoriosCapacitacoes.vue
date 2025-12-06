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
      
      <!-- Filtros poderiam ser adicionados aqui -->

      <DataTable 
        :headers="headers" 
        :items="items" 
        :loading="loading" 
        :error="error"
      >
        <template #item-certificado="{ item }">
          <span :class="item.certificado === 'Sim' ? 'text-green-600 font-bold' : 'text-gray-500'">
            {{ item.certificado }}
          </span>
        </template>
      </DataTable>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import DataTable from '../components/DataTable.vue';
import PageHeader from '../components/PageHeader.vue';
import Button from '../components/Button.vue';
import { useToast } from 'vue-toastification';

const loading = ref(true);
const downloadingExcel = ref(false);
const downloadingPdf = ref(false);
const error = ref<Error | null>(null);
const items = ref<any[]>([]);
const toast = useToast();

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
    const { data } = await api.get('/api/relatorios/capacitacoes');
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
    const response = await api.get(url, { responseType: 'blob' });
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

onMounted(() => {
  fetchData();
});
</script>
