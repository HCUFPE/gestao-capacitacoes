<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-2">
        <IdentificationIcon class="h-6 w-6" />
        <h1 class="text-2xl font-bold">Meus Cursos</h1>
      </div>
    </template>

    <div v-if="loading" class="text-center">
      <p>Carregando...</p>
    </div>

    <div v-else-if="error" class="text-center text-red-500">
      <p>Ocorreu um erro ao carregar os cursos: {{ error.message }}</p>
    </div>

    <div v-else-if="atribuicoes.length === 0" class="text-center text-gray-500">
      <p>Nenhum curso foi atribuído a você ainda.</p>
    </div>

    <div v-else class="space-y-4">
      <Card v-for="atribuicao in atribuicoes" :key="atribuicao.id">
        <div class="grid grid-cols-12 gap-4 items-center">
          <div class="col-span-12 md:col-span-6">
            <h3 class="text-lg font-semibold">{{ atribuicao.curso.titulo }}</h3>
            <p class="text-sm text-gray-600">Carga Horária: {{ atribuicao.curso.carga_horaria }}h</p>
            <p class="text-sm text-gray-600">Ano GD: {{ atribuicao.curso.ano_gd }}</p>
          </div>
          <div class="col-span-12 md:col-span-3 text-center">
            <span
              class="px-3 py-1 text-sm font-semibold rounded-full"
              :class="getStatusClass(atribuicao.status)"
            >
              {{ atribuicao.status }}
            </span>
          </div>
          <div class="col-span-12 md:col-span-3 flex justify-end space-x-2">
            <Button v-if="atribuicao.status === 'Pendente'" variant="primary">
              Enviar Certificado
            </Button>
            <Button v-else variant="secondary" disabled>
              Ver Detalhes
            </Button>
          </div>
        </div>
      </Card>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import { IdentificationIcon } from '@heroicons/vue/24/outline';

const atribuicoes = ref<any[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);

const fetchMinhasAtribuicoes = async () => {
  try {
    loading.value = true;
    error.value = null;
    const { data } = await api.get('/api/atribuicoes/me');
    atribuicoes.value = data;
  } catch (err: any) {
    error.value = err;
    console.error("Erro ao buscar atribuições:", err);
  } finally {
    loading.value = false;
  }
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Pendente':
      return 'bg-yellow-200 text-yellow-800';
    case 'Realizado':
      return 'bg-blue-200 text-blue-800';
    case 'Validado':
      return 'bg-green-200 text-green-800';
    case 'Recusado':
      return 'bg-red-200 text-red-800';
    default:
      return 'bg-gray-200 text-gray-800';
  }
};

onMounted(() => {
  fetchMinhasAtribuicoes();
});
</script>