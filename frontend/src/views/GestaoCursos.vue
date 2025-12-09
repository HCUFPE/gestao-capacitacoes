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

      <!-- Filter Bar -->
      <FilterBar 
        :filters="filterDefinitions"
        @apply-filters="applyFilters"
        @clear-filters="clearFilters"
      />

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

        <!-- Pagination -->
        <Pagination 
          v-model:currentPage="page"
          :total-pages="totalPages"
          :total-items="total"
        />
      </div>
    </Card>

    <!-- Create/Edit Modal -->
    <Modal :show="isModalOpen" @close="closeModal" size="4xl">
      <template #header>
        <h2 class="text-xl font-semibold">{{ isEditing ? 'Editar Curso' : 'Criar Novo Curso' }}</h2>
      </template>
      
      <Form ref="myForm" :key="formKey" @submit="handleSubmit" :validation-schema="validationSchema" :initial-values="initialFormValues" id="vee-form" class="mt-4">
        <div class="grid grid-cols-12 gap-4">
          <!-- Row 1: Identificação Principal -->
          <div class="col-span-12 md:col-span-6 form-group">
            <label for="titulo" class="form-label block text-sm font-medium text-paper-text mb-1">Título do Curso <span class="text-red-500">*</span></label>
            <Field name="titulo" type="text" id="titulo" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="titulo" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-4 form-group">
            <label for="tema" class="form-label block text-sm font-medium text-paper-text mb-1">Eixos Temáticos (Tema)</label>
            <Field name="tema" type="text" id="tema" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="tema" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-2 form-group">
            <label for="ano_gd" class="form-label block text-sm font-medium text-paper-text mb-1">Ano da GD</label>
            <Field name="ano_gd" as="select" id="ano_gd" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm">
              <option value="" disabled>Selecione</option>
              <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
            </Field>
            <ErrorMessage name="ano_gd" class="text-red-500 text-sm mt-1" />
          </div>
          
          <!-- Row 2: Organização e Responsáveis -->
          <div class="col-span-12 md:col-span-4 form-group">
            <label for="lotacao_id" class="form-label block text-sm font-medium text-paper-text mb-1">Lotação (opcional)</label>
            <Field name="lotacao_id" as="select" id="lotacao_id" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm">
              <option value="">Nenhuma lotação</option>
              <option v-for="lotacao in lotacoesList" :key="lotacao" :value="lotacao">{{ lotacao }}</option>
            </Field>
            <ErrorMessage name="lotacao_id" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-4 form-group">
            <label for="certificadora" class="form-label block text-sm font-medium text-paper-text mb-1">Certificadora</label>
            <Field name="certificadora" type="text" id="certificadora" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="certificadora" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-4 form-group">
            <label for="conteudista" class="form-label block text-sm font-medium text-paper-text mb-1">Conteudista</label>
            <Field name="conteudista" type="text" id="conteudista" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="conteudista" class="text-red-500 text-sm mt-1" />
          </div>

          <!-- Row 3: Detalhes Técnicos -->
          <div class="col-span-6 md:col-span-3 form-group">
            <label for="carga_horaria" class="form-label block text-sm font-medium text-paper-text mb-1">Carga Horária</label>
            <Field name="carga_horaria" type="number" id="carga_horaria" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="carga_horaria" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-6 md:col-span-3 form-group">
            <label for="disponibilidade_dias" class="form-label block text-sm font-medium text-paper-text mb-1">Disponibilidade (dias)</label>
            <Field name="disponibilidade_dias" type="number" id="disponibilidade_dias" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="disponibilidade_dias" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-3 form-group">
            <label for="tipo_oferta" class="form-label block text-sm font-medium text-paper-text mb-1">Tipo de Oferta</label>
            <Field name="tipo_oferta" type="text" id="tipo_oferta" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="tipo_oferta" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-3 form-group">
            <label for="data_lancamento" class="form-label block text-sm font-medium text-paper-text mb-1">Data Lançamento</label>
            <Field name="data_lancamento" type="text" id="data_lancamento" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" placeholder="YYYY-MM-DD" />
            <ErrorMessage name="data_lancamento" class="text-red-500 text-sm mt-1" />
          </div>

          <!-- Row 4: Acesso -->
          <div class="col-span-12 md:col-span-8 form-group">
            <label for="link" class="form-label block text-sm font-medium text-paper-text mb-1">Link para Inscrição</label>
            <Field name="link" type="url" id="link" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" placeholder="https://exemplo.com/inscricao" />
            <ErrorMessage name="link" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-4 form-group">
            <label for="acessibilidade" class="form-label block text-sm font-medium text-paper-text mb-1">Acessibilidade</label>
            <Field name="acessibilidade" type="text" id="acessibilidade" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm" />
            <ErrorMessage name="acessibilidade" class="text-red-500 text-sm mt-1" />
          </div>

          <!-- Row 5: Descrições (Full Width) -->
          <div class="col-span-12 md:col-span-6 form-group">
            <label for="apresentacao" class="form-label block text-sm font-medium text-paper-text mb-1">Apresentação</label>
            <Field name="apresentacao" as="textarea" id="apresentacao" rows="3" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm"></Field>
            <ErrorMessage name="apresentacao" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-6 form-group">
            <label for="publico_alvo" class="form-label block text-sm font-medium text-paper-text mb-1">Público Alvo</label>
            <Field name="publico_alvo" as="textarea" id="publico_alvo" rows="3" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm"></Field>
            <ErrorMessage name="publico_alvo" class="text-red-500 text-sm mt-1" />
          </div>

          <div class="col-span-12 md:col-span-6 form-group">
            <label for="conteudo_programatico" class="form-label block text-sm font-medium text-paper-text mb-1">Conteúdo Programático</label>
            <Field name="conteudo_programatico" as="textarea" id="conteudo_programatico" rows="3" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm"></Field>
            <ErrorMessage name="conteudo_programatico" class="text-red-500 text-sm mt-1" />
          </div>
          
          <div class="col-span-12 md:col-span-6 form-group">
            <label for="observacao" class="form-label block text-sm font-medium text-paper-text mb-1">Observação</label>
            <Field name="observacao" as="textarea" id="observacao" rows="3" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm"></Field>
            <ErrorMessage name="observacao" class="text-red-500 text-sm mt-1" />
          </div>

          <!-- Checkbox for assigning to all -->
          <div class="col-span-12 form-group mt-2">
            <div class="flex items-center">
              <input
                type="checkbox"
                id="atribuir_a_todos"
                class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                :checked="myForm?.values.atribuir_a_todos"
                @change="event => { if (myForm) myForm.setFieldValue('atribuir_a_todos', (event.target as HTMLInputElement).checked) }"
              />
              <label for="atribuir_a_todos" class="ml-2 block text-sm text-gray-900">
                Atribuir este curso a todos os funcionários deste setor
              </label>
            </div>
            <p class="text-xs text-gray-500 mt-1">Se marcado, o curso será atribuído a todos no setor que ainda não o possuem.</p>
          </div>
        </div>
      </Form>
      
      <template #footer>
        <div class="flex justify-end space-x-4">
          <Button type="button" @click="closeModal" variant="default">
            <template #icon><XMarkIcon class="h-5 w-5" /></template>
            Cancelar
          </Button>
          <Button form="vee-form" type="submit" variant="primary" :loading="isSubmitting">
            <template #icon><CheckIcon class="h-5 w-5" /></template>
            Salvar
          </Button>
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
          <Button type="button" @click="closeConfirmModal" variant="default">
            <template #icon><XMarkIcon class="h-5 w-5" /></template>
            Cancelar
          </Button>
          <Button @click="confirmDelete" variant="danger" :loading="isDeleting">
            <template #icon><TrashIcon class="h-5 w-5" /></template>
            Excluir
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import * as z from 'zod';
import { useToast } from 'vue-toastification';
import { PlusIcon, AcademicCapIcon, PencilIcon, TrashIcon, LinkIcon, CheckIcon, XMarkIcon, TagIcon } from '@heroicons/vue/24/outline';

import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import DataTable from '../components/DataTable.vue';
import PageHeader from '../components/PageHeader.vue';
import Pagination from '../components/Pagination.vue';
import FilterBar from '../components/FilterBar.vue';

const toast = useToast();

const tableHeaders = ref([
  { text: 'Título', value: 'titulo' },
  { text: 'Tema', value: 'tema' },
  { text: 'Certificadora', value: 'certificadora' },
  { text: 'CH', value: 'carga_horaria' },
  { text: 'Lotação', value: 'lotacao_id' },
  { text: 'Ano GD', value: 'ano_gd' },
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

// Pagination and Filter State
const page = ref(1);
const limit = ref(10);
const total = ref(0);
const activeFilters = ref<Record<string, string>>({});

// Filter definitions for FilterBar
const filterDefinitions = ref([
  { key: 'titulo', label: 'Título', placeholder: 'Buscar por título...', icon: AcademicCapIcon },
  { key: 'tema', label: 'Tema', placeholder: 'Buscar por tema...', icon: TagIcon },
]);

const totalPages = computed(() => Math.ceil(total.value / limit.value));

const initialFormValues = ref({
  titulo: '',
  tema: '',
  lotacao_id: '',
  ano_gd: new Date().getFullYear().toString(),
  carga_horaria: undefined,
  certificadora: '',
  link: '',
  conteudista: '',
  disponibilidade_dias: undefined,
  tipo_oferta: '',
  apresentacao: '',
  publico_alvo: '',
  conteudo_programatico: '',
  data_lancamento: '',
  acessibilidade: '',
  observacao: '',
  atribuir_a_todos: false,
});

const validationSchema = toTypedSchema(
  z.object({
    titulo: z.string().nonempty('O título é obrigatório'),
    tema: z.string().optional().nullable(),
    lotacao_id: z.string().optional().nullable(),
    ano_gd: z.string().nonempty('O ano é obrigatório'),
    carga_horaria: z.number().int("Deve ser um número inteiro").optional().nullable().or(z.literal('')),
    certificadora: z.string().optional().nullable(),
    link: z.string().url('Link inválido').optional().or(z.literal('')),
    conteudista: z.string().optional().nullable(),
    disponibilidade_dias: z.number().int("Deve ser um número inteiro").optional().nullable().or(z.literal('')),
    tipo_oferta: z.string().optional().nullable(),
    apresentacao: z.string().optional().nullable(),
    publico_alvo: z.string().optional().nullable(),
    conteudo_programatico: z.string().optional().nullable(),
    data_lancamento: z.string().optional().nullable(),
    acessibilidade: z.string().optional().nullable(),
    observacao: z.string().optional().nullable(),
    atribuir_a_todos: z.boolean().default(false),
  }).transform((obj) => {
    // Transforma strings vazias em null para números
    if (obj.carga_horaria === '') obj.carga_horaria = null;
    if (obj.disponibilidade_dias === '') obj.disponibilidade_dias = null;
    return obj;
  })
);


watch(isModalOpen, (isOpen) => {
  if (isOpen) {
    nextTick(() => {
      // Ensure the checkbox state is set correctly from initialFormValues
      if (myForm.value) {
        myForm.value.setFieldValue('atribuir_a_todos', initialFormValues.value.atribuir_a_todos);
      }
    });
  }
});

const availableYears = computed(() => {
  const currentYear = new Date().getFullYear();
  const years = [];
  for (let i = currentYear - 5; i <= currentYear + 5; i++) { // Range de 10 anos
    years.push(i.toString());
  }
  return years;
});

const fetchCursos = async () => {
  try {
    loading.value = true;
    const params = {
      skip: (page.value - 1) * limit.value,
      limit: limit.value,
      ...activeFilters.value
    };
    const { data } = await api.get('/api/cursos', { params });
    cursos.value = data.items;
    total.value = data.total;
    dataLoaded.value = true;
  } catch (err: any) {
    error.value = err;
    toast.error('Falha ao carregar os cursos.');
  } finally {
    loading.value = false;
  }
};

const applyFilters = (filters: Record<string, string>) => {
  page.value = 1;
  activeFilters.value = filters;
  fetchCursos();
};

const clearFilters = () => {
  page.value = 1;
  activeFilters.value = {};
  fetchCursos();
};

watch(page, fetchCursos);

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

const formKey = ref(0); // Key to force re-render Form component

const openCreateModal = () => {
  isEditing.value = false;
  editingCursoId.value = null;
  initialFormValues.value = {
    titulo: '',
    tema: '',
    lotacao_id: '',
    ano_gd: new Date().getFullYear().toString(),
    carga_horaria: undefined,
    certificadora: '',
    link: '',
    conteudista: '',
    disponibilidade_dias: undefined,
    tipo_oferta: '',
    apresentacao: '',
    publico_alvo: '',
    conteudo_programatico: '',
    data_lancamento: '',
    acessibilidade: '',
    observacao: '',
    atribuir_a_todos: false,
  };
  formKey.value++; // Increment key to force re-render form
  isModalOpen.value = true;
};

const myForm = ref<any>(null); // Ref to access VeeValidate form instance

const openEditModal = (curso: any) => {
  isEditing.value = true;
  editingCursoId.value = curso.id;
  initialFormValues.value = {
    titulo: curso.titulo,
    tema: curso.tema || '',
    lotacao_id: curso.lotacao_id || '',
    ano_gd: curso.ano_gd || new Date().getFullYear().toString(),
    carga_horaria: curso.carga_horaria,
    certificadora: curso.certificadora || '',
    link: curso.link || '',
    conteudista: curso.conteudista || '',
    disponibilidade_dias: curso.disponibilidade_dias,
    tipo_oferta: curso.tipo_oferta || '',
    apresentacao: curso.apresentacao || '',
    publico_alvo: curso.publico_alvo || '',
    conteudo_programatico: curso.conteudo_programatico || '',
    data_lancamento: curso.data_lancamento || '',
    acessibilidade: curso.acessibilidade || '',
    observacao: curso.observacao || '',
    atribuir_a_todos: curso.atribuir_a_todos,
  };
  formKey.value++; // Increment key to force re-render form
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
  console.log('Submitting values:', values);
  isSubmitting.value = true;
  try {
    const payload = { ...values };

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
