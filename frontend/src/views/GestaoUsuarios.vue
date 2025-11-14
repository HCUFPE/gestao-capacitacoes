<template>
  <div>
    <Card>
      <template #header>
        <PageHeader title="Gestão de Usuários" :icon="UsersIcon" />
      </template>

      <!-- Reusable Filter Bar -->
      <FilterBar 
        :filters="filterDefinitions"
        @apply-filters="applyFilters"
        @clear-filters="clearFilters"
      />

      <!-- Loading/Error/Empty States -->
      <div v-if="loading" class="text-center py-10">
        <p>Carregando usuários...</p>
      </div>
      <div v-else-if="error" class="text-center py-10 text-red-500">
        <p>Ocorreu um erro ao carregar os usuários: {{ error.message }}</p>
      </div>
      <div v-else-if="users.length === 0" class="text-center py-10 text-gray-500">
        <p>Nenhum usuário encontrado.</p>
      </div>

      <!-- Users Table -->
      <div v-else class="mt-4">
        <DataTable :headers="tableHeaders" :items="users">
          <template #actions="{ item }">
            <Button @click="openEditModal(item)" variant="secondary" size="sm" type="button" title="Editar">
              <template #icon><PencilIcon class="h-4 w-4" /></template>
            </Button>
          </template>
        </DataTable>

        <!-- Reusable Pagination -->
        <Pagination 
          v-model:currentPage="currentPage"
          :total-pages="totalPages"
          :total-items="totalUsers"
        />
      </div>
    </Card>

    <!-- Edit User Modal -->
    <Modal :show="isModalOpen" @close="closeModal">
      <template #header>
        <h2 class="text-xl font-semibold">Editar Perfil de Usuário</h2>
      </template>
      
      <Form v-if="editingUser" @submit="handleSubmit" :validation-schema="validationSchema" :initial-values="initialFormValues" id="user-form" class="mt-4">
        <div class="space-y-4">
          <div>
            <p><strong>Usuário:</strong> {{ editingUser.displayName }}</p>
            <p><strong>Email:</strong> {{ editingUser.email }}</p>
          </div>
          <div class="form-group">
            <label for="perfil" class="form-label block text-sm font-medium text-paper-text mb-1">Perfil</label>
            <Field name="perfil" as="select" id="perfil" class="form-control block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm">
              <option v-for="profile in availableProfiles" :key="profile" :value="profile">{{ profile }}</option>
            </Field>
            <ErrorMessage name="perfil" class="text-red-500 text-sm mt-1" />
          </div>
        </div>
      </Form>
      
      <template #footer>
        <div class="flex justify-end space-x-4">
          <Button type="button" @click="closeModal" variant="default">
            <template #icon><XMarkIcon class="h-5 w-5" /></template>
            Cancelar
          </Button>
          <Button form="user-form" type="submit" variant="primary" :loading="isSubmitting">
            <template #icon><CheckIcon class="h-5 w-5" /></template>
            Salvar
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, defineAsyncComponent } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import * as z from 'zod';
import { useToast } from 'vue-toastification';
import { 
  UsersIcon, 
  PencilIcon, 
  CheckIcon, 
  XMarkIcon,
} from '@heroicons/vue/24/outline';

import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import DataTable from '../components/DataTable.vue';
import PageHeader from '../components/PageHeader.vue';
import Pagination from '../components/Pagination.vue';
import FilterBar from '../components/FilterBar.vue';

// Async load icons for filter bar for better performance
const UserIcon = defineAsyncComponent(() => import('@heroicons/vue/24/outline/UserIcon'));
const BuildingOffice2Icon = defineAsyncComponent(() => import('@heroicons/vue/24/outline/BuildingOffice2Icon'));

type UserProfile = {
  id: string;
  displayName: string;
  email: string;
  lotacao: string;
  perfil: 'Trabalhador' | 'Chefia' | 'UDP';
  course_count: number;
};

const toast = useToast();

// Refs for data and state
const users = ref<UserProfile[]>([]);
const loading = ref(false);
const error = ref<Error | null>(null);

// Refs for pagination
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalUsers = ref(0);

// Ref for filter values
const activeFilters = ref<Record<string, string>>({});

// Refs for modal
const isModalOpen = ref(false);
const isSubmitting = ref(false);
const editingUser = ref<UserProfile | null>(null);

// Filter definitions for the FilterBar component
const filterDefinitions = ref([
  { key: 'nome', label: 'Nome do Usuário', placeholder: 'Filtrar por nome...', icon: UserIcon },
  { key: 'lotacao', label: 'Lotação', placeholder: 'Filtrar por lotação...', icon: BuildingOffice2Icon },
]);

// Computed properties
const totalPages = computed(() => Math.ceil(totalUsers.value / itemsPerPage.value));

// Table headers
const tableHeaders = ref([
  { text: 'Nome', value: 'displayName' },
  { text: 'Email', value: 'email' },
  { text: 'Lotação', value: 'lotacao' },
  { text: 'Perfil', value: 'perfil' },
  { text: 'Cursos Atribuídos', value: 'course_count' },
]);

const availableProfiles = ['Trabalhador', 'Chefia', 'UDP'];

const initialFormValues = ref({
  perfil: 'Trabalhador',
});

const validationSchema = toTypedSchema(
  z.object({
    perfil: z.enum(['Trabalhador', 'Chefia', 'UDP'], {
      errorMap: () => ({ message: 'Selecione um perfil válido.' }),
    }),
  })
);

const capitalizeName = (name: string): string => {
  if (!name) return '';
  const exceptions = ['de', 'da', 'do', 'dos', 'das'];
  return name
    .toLowerCase()
    .split(' ')
    .map(word => {
      return exceptions.includes(word) ? word : word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(' ');
};

const fetchUsers = async () => {
  try {
    loading.value = true;
    const skip = (currentPage.value - 1) * itemsPerPage.value;
    
    const params: any = { 
      skip, 
      limit: itemsPerPage.value,
      ...activeFilters.value 
    };

    const { data } = await api.get('/api/admin/usuarios', { params });
    
    users.value = data.data.map((user: any) => ({
      ...user,
      displayName: capitalizeName(user.nome),
      email: user.email ? user.email.toLowerCase() : 'N/A',
    }));
    totalUsers.value = data.total_count;
  } catch (err: any) {
    error.value = err;
    toast.error('Falha ao carregar os usuários.');
  } finally {
    loading.value = false;
  }
};

const applyFilters = (filters: Record<string, string>) => {
  currentPage.value = 1;
  activeFilters.value = filters;
  fetchUsers();
};

const clearFilters = () => {
  currentPage.value = 1;
  activeFilters.value = {};
  fetchUsers();
};

const openEditModal = (user: UserProfile) => {
  editingUser.value = user;
  initialFormValues.value = {
    perfil: user.perfil,
  };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  editingUser.value = null;
};

const handleSubmit = async (values: any) => {
  if (!editingUser.value) return;

  isSubmitting.value = true;
  try {
    const payload = {
      user_id: editingUser.value.id,
      novo_perfil: values.perfil,
    };

    await api.put('/api/admin/usuarios/perfil', payload);
    toast.success('Perfil do usuário atualizado com sucesso!');
    
    closeModal();
    await fetchUsers();
  } catch (err: any) {
    toast.error(`Erro ao atualizar o perfil: ${err.response?.data?.detail || err.message}`);
  } finally {
    isSubmitting.value = false;
  }
};

// Watch for page changes from the Pagination component
watch(currentPage, fetchUsers);

onMounted(fetchUsers);
</script>
