<template>
  <div class="space-y-8">
    <PageHeader title="Validação de Certificados" />
    <Card>
      <template #header>
        <h2 class="text-xl font-semibold">Certificados Pendentes de Análise</h2>
      </template>
      <DataTable
        :headers="headers"
        :items="pendencias"
        :loading="loading"
        :error="error"
      >
        <template #item-data_submissao="{ item }">
          {{ new Date(item.data_submissao).toLocaleDateString() }}
        </template>
        <template #item-actions="{ item }">
          <div class="flex space-x-2">
            <Button variant="secondary" @click="verCertificado(item.certificado_id)">
              Ver
            </Button>
            <Button variant="success" @click="handleValidacao(item.atribuicao_id, 'VALIDADO')">
              Aprovar
            </Button>
            <Button variant="danger" @click="handleValidacao(item.atribuicao_id, 'RECUSADO')">
              Recusar
            </Button>
          </div>
        </template>
      </DataTable>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { useToast } from 'vue-toastification';
import PageHeader from '../components/PageHeader.vue';
import Card from '../components/Card.vue';
import DataTable from '../components/DataTable.vue';
import Button from '../components/Button.vue';

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();
const pendencias = ref<any[]>([]);

const headers = [
  { text: 'Colaborador', value: 'usuario_nome' },
  { text: 'Curso', value: 'curso_titulo' },
  { text: 'Data de Submissão', value: 'data_submissao' },
  { text: 'Ações', value: 'actions', sortable: false },
];

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
  try {
    await api.post('/api/certificados/validar', { atribuicao_id: atribuicaoId, status });
    toast.success(`Certificado ${status === 'VALIDADO' ? 'aprovado' : 'recusado'} com sucesso!`);
    // Remove o item da lista para atualizar a UI
    pendencias.value = pendencias.value.filter(p => p.atribuicao_id !== atribuicaoId);
  } catch (err: any) {
    toast.error(`Erro ao processar validação: ${err.response?.data?.detail || err.message}`);
  }
};

onMounted(fetchPendencias);
</script>
