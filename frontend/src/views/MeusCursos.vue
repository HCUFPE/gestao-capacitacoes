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
      <section v-if="enrolledCourses.length > 0">
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <CheckCircleIcon class="h-6 w-6 text-green-500" />
          <span>Cursos Inscritos</span>
        </h2>
        <div class="space-y-4">
          <CourseCard v-for="inscricao in enrolledCourses" :key="inscricao.id" :curso="{ ...inscricao.curso, status: inscricao.status, atribuicaoId: inscricao.atribuicao_id }" @send-certificate="handleSendCertificate">
            <template #secondary-action>
              <Button @click="handleUnenroll(inscricao.id)" variant="danger" type="button">
                <template #icon><XCircleIcon class="h-5 w-5" /></template>
                Desinscrever-se
              </Button>
            </template>
            <template #primary-action>
              <Button v-if="inscricao.status === 'Em Andamento'" variant="primary" type="button" @click="handleSendCertificate(inscricao.atribuicao_id)">
                <template #icon><ArrowUpTrayIcon class="h-5 w-5" /></template>
                Enviar Certificado
              </Button>
              <Button v-else variant="secondary" @click="openDetailsModal(inscricao)">
                <template #icon><InformationCircleIcon class="h-5 w-5" /></template>
                Ver Detalhes
              </Button>
            </template>
          </CourseCard>
        </div>
      </section>

      <!-- Cursos Atribuídos (antigas atribuições) -->
      <section v-if="filteredAssignedCourses.length > 0">
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <IdentificationIcon class="h-6 w-6 text-blue-500" />
          <span>Cursos Atribuídos</span>
        </h2>
        <div class="space-y-4">
          <CourseCard v-for="atribuicao in filteredAssignedCourses" :key="atribuicao.id" :curso="{ ...atribuicao.curso, status: atribuicao.status, atribuicaoId: atribuicao.id }" @send-certificate="handleSendCertificate">
            <template #primary-action>
              <Button v-if="atribuicao.status === 'Pendente'" variant="success" type="button" @click="handleEnroll(atribuicao.curso.id)">
                <template #icon><CheckCircleIcon class="h-5 w-5" /></template>
                Inscrever-se
              </Button>
              <Button v-else variant="secondary" @click="openDetailsModal(atribuicao)">
                <template #icon><InformationCircleIcon class="h-5 w-5" /></template>
                Ver Detalhes
              </Button>
            </template>
          </CourseCard>
        </div>
      </section>

      <!-- Cursos Recomendados -->
      <section v-if="recommendedCourses.length > 0">
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <AcademicCapIcon class="h-6 w-6 text-purple-500" />
          <span>Cursos Recomendados para sua Lotação</span>
        </h2>
        <div class="space-y-4">
          <CourseCard v-for="curso in recommendedCourses" :key="curso.id" :curso="curso">
            <template #primary-action>
              <Button @click="handleEnroll(curso.id)" variant="success" type="button">
                <template #icon><CheckCircleIcon class="h-5 w-5" /></template>
                Inscrever-se
              </Button>
            </template>
          </CourseCard>
        </div>
      </section>

      <!-- Cursos Genéricos -->
      <section v-if="genericCourses.length > 0">
        <h2 class="text-xl font-bold mb-4 flex items-center space-x-2">
          <AcademicCapIcon class="h-6 w-6 text-gray-500" />
          <span>Cursos de Interesse Geral</span>
        </h2>
        <div class="space-y-2">
          <div v-for="curso in genericCourses" :key="curso.id" class="flex items-center justify-between p-3 border border-gray-200 rounded-lg bg-gray-50">
            <div class="flex items-center space-x-3">
              <AcademicCapIcon class="h-8 w-8 text-gray-400 flex-shrink-0" />
              <div>
                <span class="text-lg leading-tight font-medium text-black">{{ curso.titulo }}</span>
                <div class="text-sm text-gray-500">
                  <span class="uppercase tracking-wide text-gray-400 font-semibold mr-2">{{ curso.ano_gd }}</span>
                  <span>Carga Horária: {{ curso.carga_horaria }}h</span>
                </div>
              </div>
            </div>
            <div class="flex space-x-2">
              <Button @click="handleEnroll(curso.id)" variant="success" type="button" size="sm">
                <template #icon><CheckCircleIcon class="h-4 w-4" /></template>
                Inscrever-se
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <CertificateUploadModal :show="isUploadModalOpen" :atribuicao-id="selectedAtribuicaoId" @close="isUploadModalOpen = false" @upload-success="onUploadSuccess" />
    <CourseDetailsModal :show="isDetailsModalOpen" :curso="selectedCourseForDetails" @close="isDetailsModalOpen = false" @send-certificate="handleSendCertificate" />
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import CourseCard from '../components/CourseCard.vue';
import CertificateUploadModal from '../components/CertificateUploadModal.vue';
import CourseDetailsModal from '../components/CourseDetailsModal.vue'; // Import new modal
import { IdentificationIcon, CheckCircleIcon, XCircleIcon, AcademicCapIcon, ArrowUpTrayIcon, InformationCircleIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';

const assignedCourses = ref<any[]>([]);
const enrolledCourses = ref<any[]>([]);
const recommendedCourses = ref<any[]>([]);
const genericCourses = ref<any[]>([]); // New ref for generic courses
const loading = ref(true);
const error = ref<Error | null>(null);
const toast = useToast();

// State for Upload Modal
const isUploadModalOpen = ref(false);
const selectedAtribuicaoId = ref<string | null>(null);

// State for Details Modal
const isDetailsModalOpen = ref(false);
const selectedCourseForDetails = ref<any | null>(null);

const enrolledCourseIds = computed(() => {
  return enrolledCourses.value.map(inscricao => inscricao.curso.id);
});

const filteredAssignedCourses = computed(() => {
  return assignedCourses.value.filter(atribuicao => !enrolledCourseIds.value.includes(atribuicao.curso.id));
});

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

const fetchGenericCourses = async () => { // New function for generic courses
  try {
    loading.value = true;
    error.value = null;
    const { data } = await api.get('/api/cursos/genericos');
    genericCourses.value = data;
  } catch (err: any) {
    error.value = err;
    console.error("Erro ao buscar cursos genéricos:", err);
  } finally {
    loading.value = false;
  }
};

const handleEnroll = async (cursoId: string) => {
  try {
    await api.post('/api/inscricoes', { curso_id: cursoId });
    toast.success('Inscrição realizada com sucesso!');
    await fetchEnrolledCourses();
    await fetchAssignedCourses(); // Refresh assigned courses
    await fetchRecommendedCourses(); // Refresh recommended to remove enrolled course
    await fetchGenericCourses(); // Refresh generic courses
  } catch (err: any) {
    toast.error(`Erro ao inscrever-se: ${err.response?.data?.detail || err.message}`);
  }
};

const handleUnenroll = async (inscricaoId: string) => {
  try {
    await api.delete(`/api/inscricoes/${inscricaoId}`);
    toast.success('Desinscrição realizada com sucesso!');
    await fetchEnrolledCourses();
    await fetchAssignedCourses(); // Refresh assigned courses
    await fetchRecommendedCourses(); // Refresh recommended to potentially show course again
    await fetchGenericCourses(); // Refresh generic courses
  } catch (err: any) {
    toast.error(`Erro ao desinscrever-se: ${err.response?.data?.detail || err.message}`);
  }
};

const handleSendCertificate = (atribuicaoId: string) => {
  isDetailsModalOpen.value = false; // Close details modal if open
  selectedAtribuicaoId.value = atribuicaoId;
  isUploadModalOpen.value = true;
};

const onUploadSuccess = () => {
  isUploadModalOpen.value = false;
  fetchAssignedCourses();
  fetchEnrolledCourses();
  fetchGenericCourses(); // Refresh generic courses
};

const openDetailsModal = (item: any) => {
  // item pode ser uma inscricao ou uma atribuicao
  const cursoData = item.curso;
  const status = item.status;
  const atribuicaoId = item.atribuicao_id || item.id; // atribuicao_id para inscricao, id para atribuicao

  selectedCourseForDetails.value = {
    ...cursoData,
    status: status,
    atribuicaoId: atribuicaoId,
    certificado_id: item.certificado_id,
    certificado_file_path: item.certificado_file_path,
    certificado_link: item.certificado_link,
  };
  isDetailsModalOpen.value = true;
};

onMounted(() => {
  fetchAssignedCourses();
  fetchEnrolledCourses();
  fetchRecommendedCourses();
  fetchGenericCourses(); // Initial fetch for generic courses
});
</script>