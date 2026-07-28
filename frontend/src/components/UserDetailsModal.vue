<template>
  <Modal :show="show" @close="$emit('close')" size="5xl">
    <template #header>
      <h2 class="text-xl font-semibold">Detalhes do Usuário: {{ userName }}</h2>
    </template>
    <div v-if="loading" class="text-center py-4">Carregando...</div>
    <div v-else-if="error" class="text-red-500 py-4">
      {{ error }}
    </div>
    <DataTable v-else :headers="cursosHeaders" :items="cursosFlat">
      <template #certificado="{ item }">
        <a
          v-if="item.certificado_file_path || item.certificado_link"
          :href="getCertificateUrl(item) ?? ''"
          target="_blank"
          class="text-blue-500 hover:text-blue-700"
        >
          Visualizar
        </a>
        <span v-else class="text-gray-400">—</span>
      </template>
    </DataTable>
    <template #footer>
      <div class="flex justify-end">
        <Button @click="$emit('close')" variant="default">
          Fechar
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import api from '../services/api';
import { getCertificateUrl } from '../services/certificateUtils';
import DataTable from './DataTable.vue';
import Modal from './Modal.vue';
import Button from './Button.vue';
import { useToast } from 'vue-toastification';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  userId: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['close']);

const toast = useToast();
const loading = ref(false);
const error = ref<string | null>(null);
const userName = ref('');
const cursos = ref<any[]>([]);

const cursosHeaders = [
  { text: 'Curso', value: 'titulo' },
  { text: 'Plataforma', value: 'plataforma' },
  { text: 'CH', value: 'carga_horaria' },
  { text: 'Ano GD', value: 'ano_gd' },
  { text: 'Status', value: 'status' },
  { text: 'Certificado', value: 'certificado' },
];

// Flatten curso data so DataTable can display it
const cursosFlat = computed(() =>
  cursos.value.map(c => ({
    id: c.id,
    titulo: c.curso?.titulo || '',
    plataforma: c.curso?.certificadora || '',
    carga_horaria: c.curso?.carga_horaria,
    ano_gd: c.curso?.ano_gd,
    status: c.status,
    certificado_file_path: c.certificado_file_path,
    certificado_link: c.certificado_link,
  }))
);

const fetchUserDetails = async () => {
  if (!props.userId) return;

  loading.value = true;
  error.value = null;
  cursos.value = [];
  userName.value = '';

  try {
    const { data } = await api.get(`/api/relatorios/usuario/${props.userId}/detalhes`);
    cursos.value = data;
  } catch (err: any) {
    error.value = `Erro ao carregar detalhes: ${err.response?.data?.detail || err.message}`;
    toast.error(error.value);
  } finally {
    loading.value = false;
  }
};

// Extract user name from the first course record if available
watch(
  () => cursos.value,
  (newCursos) => {
    if (newCursos.length > 0) {
      userName.value = `ID: ${props.userId}`;
    }
  }
);

// Fetch when modal opens (userId changes or show toggles)
// immediate: true so it fires on mount when show is already true
watch(
  () => props.show,
  async (newVal) => {
    if (newVal && props.userId) {
      await fetchUserDetails();
    }
  },
  { immediate: true }
);


</script>
