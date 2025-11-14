<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-2">
        <ChartBarIcon class="h-6 w-6" />
        <h1 class="text-2xl font-bold">Relatórios UDP</h1>
      </div>
    </template>

    <div v-if="loading" class="text-center">
      <p>Carregando relatórios...</p>
    </div>

    <div v-else-if="error" class="text-center text-red-500">
      <p>Ocorreu um erro ao carregar os relatórios: {{ error.message }}</p>
    </div>

    <div v-else class="space-y-8">
      <!-- Relatório 1: Cursos Mais Inscritos/Atribuídos -->
      <section>
        <h2 class="text-xl font-semibold mb-4">Cursos Mais Inscritos/Atribuídos</h2>
        <DataTable :headers="cursosPopularesHeaders" :items="cursosPopulares" :loading="false" :error="null">
          <template #item-titulo="{ item }">
            <span class="font-medium">{{ item.titulo }}</span>
          </template>
        </DataTable>
      </section>

      <!-- Placeholder para outros relatórios UDP -->
      <section>
        <h2 class="text-xl font-semibold mb-4">Status Geral das Capacitações</h2>
        <p>Conteúdo do relatório de status geral...</p>
      </section>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import DataTable from '../components/DataTable.vue';
import { ChartBarIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();

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
    fetchCursosPopulares(),
    // Chamar outras funções de fetch para relatórios UDP aqui
  ]);
  loading.value = false;
});
</script>
