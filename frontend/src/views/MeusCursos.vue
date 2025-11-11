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

    <div v-else class="space-y-8">
      <!-- Cursos Inscritos -->
      <section>
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <CheckCircleIcon class="h-6 w-6 text-green-500" />
          <span>Cursos Inscritos</span>
        </h2>
        <div v-if="enrolledCourses.length === 0" class="text-center text-gray-500 py-4">
          <p>Você não está inscrito em nenhum curso.</p>
        </div>
        <div v-else class="space-y-4">
          <Card v-for="inscricao in enrolledCourses" :key="inscricao.id">
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-12 md:col-span-8">
                <h3 class="text-lg font-semibold">{{ inscricao.curso.titulo }}</h3>
                <p class="text-sm text-gray-600">Carga Horária: {{ inscricao.curso.carga_horaria }}h</p>
                <p class="text-sm text-gray-600">Ano GD: {{ inscricao.curso.ano_gd }}</p>
                <a v-if="inscricao.curso.link" :href="inscricao.curso.link" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:text-blue-700 text-sm flex items-center space-x-1 mt-1">
                  <LinkIcon class="h-4 w-4" />
                  <span>Link de Inscrição</span>
                </a>
              </div>
              <div class="col-span-12 md:col-span-4 flex justify-end space-x-2">
                <Button @click="handleUnenroll(inscricao.id)" variant="danger" type="button">
                  <template #icon><XCircleIcon class="h-5 w-5" /></template>
                  Desinscrever-se
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <!-- Cursos Atribuídos (antigas atribuições) -->
      <section>
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <IdentificationIcon class="h-6 w-6 text-blue-500" />
          <span>Cursos Atribuídos</span>
        </h2>
        <div v-if="assignedCourses.length === 0" class="text-center text-gray-500 py-4">
          <p>Nenhum curso foi atribuído a você.</p>
        </div>
        <div v-else class="space-y-4">
          <Card v-for="atribuicao in assignedCourses" :key="atribuicao.id">
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-12 md:col-span-6">
                <h3 class="text-lg font-semibold">{{ atribuicao.curso.titulo }}</h3>
                <p class="text-sm text-gray-600">Carga Horária: {{ atribuicao.curso.carga_horaria }}h</p>
                <p class="text-sm text-gray-600">Ano GD: {{ atribuicao.curso.ano_gd }}</p>
                <a v-if="atribuicao.curso.link" :href="atribuicao.curso.link" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:text-blue-700 text-sm flex items-center space-x-1 mt-1">
                  <LinkIcon class="h-4 w-4" />
                  <span>Link de Inscrição</span>
                </a>
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
                <Button v-if="atribuicao.status === 'Pendente'" variant="primary" type="button">
                  Enviar Certificado
                </Button>
                <Button v-else variant="secondary" disabled>
                  Ver Detalhes
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <!-- Cursos Recomendados -->
      <section>
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <AcademicCapIcon class="h-6 w-6 text-purple-500" />
          <span>Cursos Recomendados para sua Lotação</span>
        </h2>
        <div v-if="recommendedCourses.length === 0" class="text-center text-gray-500 py-4">
          <p>Nenhum curso recomendado para sua lotação.</p>
        </div>
        <div v-else class="space-y-4">
          <Card v-for="curso in recommendedCourses" :key="curso.id">
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-12 md:col-span-8">
                <h3 class="text-lg font-semibold">{{ curso.titulo }}</h3>
                <p class="text-sm text-gray-600">Carga Horária: {{ curso.carga_horaria }}h</p>
                <p class="text-sm text-gray-600">Ano GD: {{ curso.ano_gd }}</p>
                <a v-if="curso.link" :href="curso.link" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:text-blue-700 text-sm flex items-center space-x-1 mt-1">
                  <LinkIcon class="h-4 w-4" />
                  <span>Link de Inscrição</span>
                </a>
              </div>
              <div class="col-span-12 md:col-span-4 flex justify-end space-x-2">
                <Button @click="handleEnroll(curso.id)" variant="success" type="button">
                  <template #icon><CheckCircleIcon class="h-5 w-5" /></template>
                  Inscrever-se
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </section>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import { IdentificationIcon, CheckCircleIcon, XCircleIcon, LinkIcon, AcademicCapIcon } from '@heroicons/vue/24/outline';

const assignedCourses = ref<any[]>([]);
const enrolledCourses = ref<any[]>([]);
const recommendedCourses = ref<any[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);

const fetchAssignedCourses = async () => {
  try {
    loading.value = true;
    error.value = null;
    const { data } = await api.get('/api/atribuicoes/me');
    assignedCourses.value = data;
  } catch (err: any) {
    error.value = err;
    console.error("Erro ao buscar atribuições:", err);
  } finally {
    loading.value = false;
  }
};

const fetchEnrolledCourses = async () => {
  try {
    loading.value = true;
    error.value = null;
    const { data } = await api.get('/api/inscricoes/me');
    enrolledCourses.value = data;
  } catch (err: any) {
    error.value = err;
    console.error("Erro ao buscar inscrições:", err);
  } finally {
    loading.value = false;
  }
};

const fetchRecommendedCourses = async () => {
  try {
    loading.value = true;
    error.value = null;
    const { data } = await api.get('/api/cursos/recommended');
    recommendedCourses.value = data;
  } catch (err: any) {
    error.value = err;
    console.error("Erro ao buscar cursos recomendados:", err);
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

const handleEnroll = async (cursoId: string) => {
  try {
    await api.post('/api/inscricoes', { curso_id: cursoId });
    toast.success('Inscrição realizada com sucesso!');
    await fetchEnrolledCourses();
    await fetchRecommendedCourses(); // Refresh recommended to remove enrolled course
  } catch (err: any) {
    toast.error(`Erro ao inscrever-se: ${err.response?.data?.detail || err.message}`);
  }
};

const handleUnenroll = async (inscricaoId: string) => {
  try {
    await api.delete(`/api/inscricoes/${inscricaoId}`);
    toast.success('Desinscrição realizada com sucesso!');
    await fetchEnrolledCourses();
    await fetchRecommendedCourses(); // Refresh recommended to potentially show course again
  } catch (err: any) {
    toast.error(`Erro ao desinscrever-se: ${err.response?.data?.detail || err.message}`);
  }
};

onMounted(() => {
  fetchAssignedCourses();
  fetchEnrolledCourses();
  fetchRecommendedCourses();
});
</script>