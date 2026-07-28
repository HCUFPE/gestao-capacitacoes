<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import Modal from './Modal.vue';
import Button from './Button.vue';
import { LinkIcon, ArrowUpTrayIcon, DocumentArrowDownIcon, EyeIcon, GlobeAltIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
import { useToast } from 'vue-toastification';
import { getCertificateUrl as getCertificateUrlUtil } from '../services/certificateUtils';

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

const emit = defineEmits(['close', 'send-certificate', 'reupload-certificate']);

const toast = useToast();
const certificateError = ref<string | null>(null);

const hasCertificate = computed(() => {
  const curso = props.curso;
  return !!curso?.certificado_id || !!curso?.certificado_file_path || !!curso?.certificado_link;
});

const showReuploadButton = computed(() => {
  if (!hasCertificate.value) return false;
  const curso = props.curso;
  if (!curso) return false;
  const reuploadStatuses = ['Realizado', 'Recusado'];
  return reuploadStatuses.includes(curso.status || '');
});

// Reset error when modal opens or course changes
watch([() => props.show, () => props.curso?.id], () => {
  certificateError.value = null;
});

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
  return getCertificateUrlUtil(curso);
});

const certificateButtonText = computed(() => {
  const curso = props.curso;
  if (!curso || !certificateUrl.value) return '';
  if (curso.certificado_file_path?.endsWith('.pdf')) {
    return 'Visualizar Certificado';
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
    return EyeIcon;
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
  const validStatuses = ['Realizado', 'Concluído', 'Validado'];
  const hasValidStatus = validStatuses.includes(curso.status || '');

  return hasCertificateUrl && hasValidStatus;
});

const handleCertificateButtonClick = () => {
  certificateError.value = null;

  if (!certificateUrl.value) return;

  // Abre diretamente em nova aba — o backend retornará 404 se o arquivo não existir
  window.open(certificateUrl.value, '_blank');
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
          <Button v-if="showReuploadButton" type="button" @click="emit('reupload-certificate', props.curso?.atribuicaoId)" variant="warning">
            <template #icon><ArrowUpTrayIcon class="h-5 w-5" /></template>
            Reenviar Certificado
          </Button>
          <Button v-if="curso?.status === 'Em Andamento'" type="button" @click="handleSendCertificateClick" variant="primary">
            <template #icon><ArrowUpTrayIcon class="h-5 w-5" /></template>
            Enviar Certificado
          </Button>
        </div>
      </div>
      <div v-if="certificateError" class="mt-3 flex items-center space-x-2 text-sm text-red-600">
        <ExclamationTriangleIcon class="h-5 w-5" />
        <span>{{ certificateError }}</span>
      </div>
    </template>
  </Modal>
</template>
