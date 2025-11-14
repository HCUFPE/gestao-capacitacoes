<script setup lang="ts">
import { computed } from 'vue';
import Modal from './Modal.vue';
import Button from './Button.vue';
import { LinkIcon, ArrowUpTrayIcon, DocumentArrowDownIcon, EyeIcon, GlobeAltIcon } from '@heroicons/vue/24/outline';

const props = defineProps<{
  show: boolean;
  curso: {
    id: string;
    titulo: string;
    carga_horaria: number;
    ano_gd: string;
    link?: string;
    status?: string;
    certificadora?: string;
    atribuicaoId?: string;
    certificado_id?: string;
    certificado_file_path?: string;
    certificado_link?: string;
  } | null;
}>();

const emit = defineEmits(['close', 'send-certificate']);

const handleSendCertificateClick = () => {
  if (props.curso?.atribuicaoId) {
    emit('send-certificate', props.curso.atribuicaoId);
  }
};

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Pendente':
      return 'bg-yellow-200 text-yellow-800';
    case 'Em Andamento':
      return 'bg-blue-200 text-blue-800';
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

const certificateUrl = computed(() => {
  const curso = props.curso;
  if (!curso) return null;

  const backendBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  if (curso.certificado_file_path) {
    // Extrair apenas o nome do arquivo do caminho completo
    const fileName = curso.certificado_file_path.split('/').pop();
    return `${backendBaseUrl}/api/certificados/download/${fileName}`;
  }
  if (curso.certificado_link) {
    return curso.certificado_link;
  }
  return null;
});

const certificateButtonText = computed(() => {
  const curso = props.curso;
  if (!curso || !certificateUrl.value) return '';
  if (curso.certificado_file_path?.endsWith('.pdf')) {
    return 'Baixar Certificado';
  }
  if (curso.certificado_file_path) {
    return 'Visualizar Certificado';
  }
  if (curso.certificado_link) {
    return 'Ver Certificado Online';
  }
  return '';
});

const certificateButtonIcon = computed(() => {
  const curso = props.curso;
  if (!curso || !certificateUrl.value) return null;
  if (curso.certificado_file_path?.endsWith('.pdf')) {
    return DocumentArrowDownIcon;
  }
  if (curso.certificado_file_path) {
    return EyeIcon;
  }
  if (curso.certificado_link) {
    return GlobeAltIcon;
  }
  return null;
});

const showCertificateButton = computed(() => {
  const curso = props.curso;
  if (!curso) return false;

  const hasCertificateUrl = !!certificateUrl.value;
  const isRealizadoOrValidado = ['REALIZADO', 'VALIDADO'].includes(curso.status || '');

  return hasCertificateUrl && isRealizadoOrValidado;
});

const handleCertificateButtonClick = () => {
  if (certificateUrl.value) {
    window.open(certificateUrl.value, '_blank');
  }
};
</script>

<template>
  <Modal :show="show" @close="$emit('close')">
    <template #header>
      <h2 class="text-xl font-semibold">Detalhes do Curso</h2>
    </template>

    <div v-if="curso" class="mt-4 space-y-4">
      <h3 class="text-2xl font-bold text-paper-text">{{ curso.titulo }}</h3>
      
      <div class="border-t border-gray-200 pt-4">
        <dl class="space-y-2">
          <div class="flex justify-between">
            <dt class="font-medium text-gray-500">Status</dt>
            <dd v-if="curso.status" class="px-3 py-1 text-sm font-semibold rounded-full" :class="getStatusClass(curso.status)">
              {{ curso.status }}
            </dd>
          </div>
          <div class="flex justify-between">
            <dt class="font-medium text-gray-500">Carga Horária</dt>
            <dd class="text-paper-text">{{ curso.carga_horaria }}h</dd>
          </div>
          <div v-if="curso.certificadora" class="flex justify-between">
            <dt class="font-medium text-gray-500">Certificadora</dt>
            <dd class="text-paper-text">{{ curso.certificadora }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="font-medium text-gray-500">Ano GD</dt>
            <dd class="text-paper-text">{{ curso.ano_gd }}</dd>
          </div>
        </dl>
      </div>

      <div v-if="curso.link" class="border-t border-gray-200 pt-4">
        <a :href="curso.link" target="_blank" rel="noopener noreferrer">
          <Button variant="secondary" class="w-full justify-center">
            <template #icon><LinkIcon class="h-5 w-5" /></template>
            Página do Curso
          </Button>
        </a>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-between items-center w-full">
        <Button type="button" @click="$emit('close')" variant="default">
          Fechar
        </Button>
        <div class="flex space-x-2">
          <Button v-if="showCertificateButton" type="button" @click="handleCertificateButtonClick" variant="info">
            <template #icon>
              <component :is="certificateButtonIcon" class="h-5 w-5" />
            </template>
            {{ certificateButtonText }}
          </Button>
          <Button v-if="curso?.status === 'Em Andamento'" type="button" @click="handleSendCertificateClick" variant="primary">
            <template #icon><ArrowUpTrayIcon class="h-5 w-5" /></template>
            Enviar Certificado
          </Button>
        </div>
      </div>
    </template>
  </Modal>
</template>
