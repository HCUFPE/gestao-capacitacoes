<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-2">
        <ChartBarIcon class="h-6 w-6" />
        <h1 class="text-2xl font-bold">Relatórios Chefia</h1>
      </div>
    </template>

    <div v-if="loading" class="text-center">
      <p>Carregando relatórios...</p>
    </div>

    <div v-else-if="error" class="text-center text-red-500">
      <p>Ocorreu um erro ao carregar os relatórios: {{ error.message }}</p>
    </div>

    <div v-else class="space-y-8">
      <!-- Relatório 1: Status de Cursos da Minha Lotação -->
      <section>
        <h2 class="text-xl font-semibold mb-4">Status de Cursos da Minha Lotação</h2>
        <p>Conteúdo do relatório de status da lotação...</p>
      </section>

      <!-- Placeholder para outros relatórios Chefia -->
      <section>
        <h2 class="text-xl font-semibold mb-4">Progresso Individual de Subordinados</h2>
        <p>Conteúdo do relatório de progresso individual...</p>
      </section>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import { ChartBarIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';

const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();

onMounted(async () => {
  loading.value = true;
  // Chamar funções de fetch para relatórios Chefia aqui
  loading.value = false;
});
</script>
