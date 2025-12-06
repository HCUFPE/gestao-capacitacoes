<template>
  <div class="space-y-8">
    <PageHeader title="Validação de Certificados" />
    <Card>
      <template #header>
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <h2 class="text-xl font-semibold">Certificados Pendentes de Análise</h2>
          <div class="relative max-w-xs w-full">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar por colaborador ou curso..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>
      </template>

      <DataTable
        :headers="headers"
        :items="paginatedPendencias"
        :loading="loading"
        :error="error"
      >
        <template #item-data_submissao="{ item }">
          {{ new Date(item.data_submissao).toLocaleDateString() }}
        </template>
        <template #item-actions="{ item }">
          <div class="flex space-x-2">
            <Button variant="secondary" size="sm" @click="verCertificado(item.certificado_id)">
              Ver
            </Button>
            <Button 
              variant="success" 
              size="sm"
              :loading="processingIds.has(item.atribuicao_id)"
              :disabled="processingIds.has(item.atribuicao_id)"
              @click="handleValidacao(item.atribuicao_id, 'VALIDADO')"
            >
              Aprovar
            </Button>
            <Button 
              variant="danger" 
              size="sm"
              :loading="processingIds.has(item.atribuicao_id)"
              :disabled="processingIds.has(item.atribuicao_id)"
              @click="handleValidacao(item.atribuicao_id, 'RECUSADO')"
            >
              Recusar
            </Button>
          </div>
        </template>
      </DataTable>

      <Pagination
        v-if="totalPages > 1"
        v-model:currentPage="currentPage"
        :totalPages="totalPages"
        :totalItems="filteredPendencias.length"
      />
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';
import { useToast } from 'vue-toastification';
import PageHeader from '../components/PageHeader.vue';
import Card from '../components/Card.vue';
import DataTable from '../components/DataTable.vue';
import Button from '../components/Button.vue';
import Pagination from '../components/Pagination.vue';

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();
const pendencias = ref<any[]>([]);
const processingIds = ref(new Set<string>());

// Filtros e Paginação
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 10;

const headers = [
  { text: 'Colaborador', value: 'usuario_nome' },
  { text: 'Curso', value: 'curso_titulo' },
  { text: 'Data de Submissão', value: 'data_submissao' },
  { text: 'Ações', value: 'actions', sortable: false },
];

const filteredPendencias = computed(() => {
  if (!searchQuery.value) return pendencias.value;
  const lower = searchQuery.value.toLowerCase();
  return pendencias.value.filter(p => 
    p.usuario_nome.toLowerCase().includes(lower) || 
    p.curso_titulo.toLowerCase().includes(lower)
  );
});

const totalPages = computed(() => Math.ceil(filteredPendencias.value.length / itemsPerPage));

const paginatedPendencias = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredPendencias.value.slice(start, start + itemsPerPage);
});

const fetchPendencias = async () => {
  loading.value = true;
  try {
    const { data } = await api.get('/api/atribuicoes/pendentes-validacao');
    pendencias.value = data;
  } catch (err: any) {
    error.value = err;
    toast.error(`Erro ao carregar pendências: ${err.response?.data?.detail || err.message}`);
  } finally {
    loading.value = false;
  }
};

const verCertificado = async (certificadoId: string) => {
  if (!certificadoId) {
    toast.error('Este certificado não possui um arquivo ou link para visualização.');
    return;
  }
  try {
    const { data: certificado } = await api.get(`/api/certificados/${certificadoId}`);
    const url = certificado.file_path 
      ? `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/certificados/download/${certificado.file_path.split('/').pop()}`
      : certificado.link;
    
    if (url) {
      window.open(url, '_blank');
    } else {
      toast.error('Não foi possível encontrar um arquivo ou link para este certificado.');
    }
  } catch (err: any) {
    toast.error(`Erro ao obter detalhes do certificado: ${err.response?.data?.detail || err.message}`);
  }
};

const handleValidacao = async (atribuicaoId: string, status: 'VALIDADO' | 'RECUSADO') => {
  processingIds.value.add(atribuicaoId);
  try {
    await api.post('/api/certificados/validar', { atribuicao_id: atribuicaoId, status });
    toast.success(`Certificado ${status === 'VALIDADO' ? 'aprovado' : 'recusado'} com sucesso!`);
    // Remove o item da lista para atualizar a UI
    pendencias.value = pendencias.value.filter(p => p.atribuicao_id !== atribuicaoId);
    
    // Ajusta a página se esvaziar
    if (paginatedPendencias.value.length === 0 && currentPage.value > 1) {
      currentPage.value--;
    }
  } catch (err: any) {
    toast.error(`Erro ao processar validação: ${err.response?.data?.detail || err.message}`);
  } finally {
    processingIds.value.delete(atribuicaoId);
  }
};

onMounted(fetchPendencias);
</script>