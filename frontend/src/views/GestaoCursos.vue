<template>
  <div>
    <Card>
      <template #header>
        <PageHeader title="Gestão de Cursos" :icon="AcademicCapIcon" />
      </template>

      <div class="flex justify-end mb-4">
        <Button @click="openCreateModal" variant="primary" type="button">
          <template #icon><PlusIcon class="h-5 w-5" /></template>
          Criar Novo Curso
        </Button>
      </div>

      <!-- Loading/Error/Empty States -->
      <div v-if="loading" class="text-center py-10">
        <p>Carregando cursos...</p>
      </div>
      <div v-else-if="error" class="text-center py-10 text-red-500">
        <p>Ocorreu um erro ao carregar os cursos: {{ error.message }}</p>
      </div>
      <div v-else-if="cursos.length === 0" class="text-center py-10 text-gray-500">
        <p>Nenhum curso encontrado. Crie o primeiro!</p>
      </div>

      <!-- Courses Table -->
      <div v-else class="mt-4">
        <DataTable :headers="tableHeaders" :items="cursos">
          <template #link="{ item }">
            <a v-if="item.link" :href="item.link" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:text-blue-700">
              <LinkIcon class="h-5 w-5" />
            </a>
          </template>
          <template #actions="{ item }">
            <div class="flex items-center space-x-2">
              <Button @click="openEditModal(item)" variant="secondary" size="sm" title="Editar">
                <template #icon><PencilIcon class="h-4 w-4" /></template>
              </Button>
              <Button @click="openDeleteModal(String(item.id))" variant="danger" size="sm" title="Deletar">
                <template #icon><TrashIcon class="h-4 w-4" /></template>
              </Button>
            </div>
          </template>
        </DataTable>
      </div>
    </Card>

    <!-- Create/Edit Modal -->
    <Modal :show="isModalOpen" @close="closeModal">
      <template #header>
        <h2 class="text-xl font-semibold">{{ isEditing ? 'Editar Curso' : 'Criar Novo Curso' }}</h2>
      </template>
      
      <Form @submit="handleSubmit" :validation-schema="validationSchema" :initial-values="initialFormValues" id="vee-form" class="mt-4">
        <div class="grid grid-cols-12 gap-4">
          <div class="col-span-12 form-group mb-4">
            <label for="titulo" class="form-label block text-sm font-medium text-paper-text mb-1">Título do Curso</label>
            <Field name="titulo" type="text" id="titulo" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="titulo" class="text-red-500 text-sm mt-1" />
          </div>
          
          <div class="col-span-12 md:col-span-6 form-group mb-4">
            <label for="lotacao" class="form-label block text-sm font-medium text-paper-text mb-1">Lotação</label>
            <Field name="lotacao" as="select" id="lotacao" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm">
              <option value="" disabled>Selecione uma lotação</option>
              <option v-for="lotacao in lotacoesList" :key="lotacao" :value="lotacao">{{ lotacao }}</option>
            </Field>
            <ErrorMessage name="lotacao" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-6 form-group mb-4">
            <label for="ano_gd" class="form-label block text-sm font-medium text-paper-text mb-1">Ano da GD</label>
            <Field name="ano_gd" as="select" id="ano_gd" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm">
              <option value="" disabled>Selecione o ano</option>
              <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
            </Field>
            <ErrorMessage name="ano_gd" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-6 form-group mb-4">
            <label for="carga_horaria" class="form-label block text-sm font-medium text-paper-text mb-1">Carga Horária (opcional)</label>
            <Field name="carga_horaria" type="number" id="carga_horaria" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="carga_horaria" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-6 form-group mb-4">
            <label for="certificadora" class="form-label block text-sm font-medium text-paper-text mb-1">Certificadora (opcional)</label>
            <Field name="certificadora" type="text" id="certificadora" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
          </div>

          <div class="col-span-12 form-group mb-4">
            <label for="link" class="form-label block text-sm font-medium text-paper-text mb-1">Link para Inscrição (opcional)</label>
            <Field name="link" type="url" id="link" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" placeholder="https://exemplo.com/inscricao" />
            <ErrorMessage name="link" class="text-red-500 text-sm mt-1" />
          </div>
        </div>
      </Form>
      
      <template #footer>
        <div class="flex justify-end space-x-4">
          <Button type="button" @click="closeModal" variant="default">Cancelar</Button>
          <Button form="vee-form" type="submit" variant="primary" :loading="isSubmitting">Salvar</Button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal :show="isConfirmModalOpen" @close="closeConfirmModal">
      <template #header>
        <h2 class="text-xl font-semibold text-red-600">Confirmar Exclusão</h2>
      </template>
      <p>Tem certeza de que deseja excluir este curso? Esta ação não pode ser desfeita.</p>
      <template #footer>
        <div class="flex justify-end space-x-4 mt-6">
          <Button type="button" @click="closeConfirmModal" variant="default">Cancelar</Button>
          <Button @click="confirmDelete" variant="danger" :loading="isDeleting">Excluir</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import * as z from 'zod';
import { useToast } from 'vue-toastification';
import { PlusIcon, AcademicCapIcon, PencilIcon, TrashIcon, LinkIcon } from '@heroicons/vue/24/outline';

import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import DataTable from '../components/DataTable.vue';
import PageHeader from '../components/PageHeader.vue';

const toast = useToast();
const authStore = useAuthStore();

const tableHeaders = ref([
  { text: 'Título', value: 'titulo' },
  { text: 'Setor', value: 'lotacao' },
  { text: 'Ano', value: 'ano_gd' },
  { text: 'Inscrição', value: 'link' },
]);

const cursos = ref<any[]>([]);
const lotacoesList = ref<string[]>([]);
const loading = ref(false);
const error = ref<Error | null>(null);
const dataLoaded = ref(false);
const isModalOpen = ref(false);
const isEditing = ref(false);
const isSubmitting = ref(false);
const editingCursoId = ref<string | null>(null);
const isConfirmModalOpen = ref(false);
const cursoToDeleteId = ref<string | null>(null);
const isDeleting = ref(false);

const initialFormValues = ref({
  titulo: '',
  lotacao: '',
  ano_gd: new Date().getFullYear(),
  carga_horaria: undefined,
  certificadora: '',
});

const validationSchema = toTypedSchema(
  z.object({
    titulo: z.string().nonempty('O título é obrigatório'),
    lotacao: z.string().nonempty('A lotação é obrigatória'),
    ano_gd: z.number({ invalid_type_error: 'O ano é obrigatório' }).int().min(1900, 'Ano inválido').max(2100, 'Ano inválido'),
    carga_horaria: z.number().int().optional().nullable(),
    certificadora: z.string().optional(),
    link: z.string().url('Link inválido').optional().or(z.literal('')),
  })
);

const availableYears = computed(() => {
  const currentYear = new Date().getFullYear();
  const years = [];
  for (let i = 0; i < 5; i++) {
    years.push(currentYear + i);
  }
  return years;
});

const fetchCursos = async () => {
  try {
    loading.value = true;
    const { data } = await api.get('/api/cursos');
    cursos.value = data;
    dataLoaded.value = true;
  } catch (err: any) {
    error.value = err;
    toast.error('Falha ao carregar os cursos.');
  } finally {
    loading.value = false;
  }
};

const fetchLotacoes = async () => {
  try {
    const { data } = await api.get('/api/utils/lotacoes');
    lotacoesList.value = data;
  } catch (err: any) {
    toast.error('Falha ao carregar a lista de lotações.');
  }
};

const loadData = async () => {
  await fetchCursos();
  await fetchLotacoes();
};

const openCreateModal = () => {
  isEditing.value = false;
  editingCursoId.value = null;
  initialFormValues.value = {
    titulo: '',
    lotacao: '',
    ano_gd: new Date().getFullYear(),
    carga_horaria: undefined,
    certificadora: '',
    link: '',
  };
  isModalOpen.value = true;
};

const openEditModal = (curso: any) => {
  isEditing.value = true;
  editingCursoId.value = curso.id;
  initialFormValues.value = {
    titulo: curso.titulo,
    lotacao: curso.lotacao,
    ano_gd: curso.ano_gd,
    carga_horaria: curso.carga_horaria,
    certificadora: curso.certificadora,
  };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const openDeleteModal = (cursoId: string) => {
  cursoToDeleteId.value = cursoId;
  isConfirmModalOpen.value = true;
};

const closeConfirmModal = () => {
  isConfirmModalOpen.value = false;
  cursoToDeleteId.value = null;
};

const confirmDelete = async () => {
  if (!cursoToDeleteId.value) return;

  isDeleting.value = true;
  try {
    await api.delete(`/api/cursos/${cursoToDeleteId.value}`);
    toast.success('Curso excluído com sucesso!');
    closeConfirmModal();
    await fetchCursos();
  } catch (err: any) {
    toast.error(`Erro ao excluir o curso: ${err.response?.data?.detail || err.message}`);
  } finally {
    isDeleting.value = false;
  }
};

const handleSubmit = async (values: any) => {
  isSubmitting.value = true;
  try {
    const payload = {
      ...values,
      ano_gd: Number(values.ano_gd),
      carga_horaria: values.carga_horaria ? Number(values.carga_horaria) : null,
      chefia_id: authStore.user?.username,
    };

    if (isEditing.value) {
      await api.put(`/api/cursos/${editingCursoId.value}`, payload);
      toast.success('Curso atualizado com sucesso!');
    } else {
      await api.post('/api/cursos', payload);
      toast.success('Curso criado com sucesso!');
    }
    
    closeModal();
    await fetchCursos();
  } catch (err: any) {
    toast.error(`Erro ao salvar o curso: ${err.response?.data?.detail || err.message}`);
  } finally {
    isSubmitting.value = false;
  }
};
onMounted(() => {
  loadData();
});
</script>
