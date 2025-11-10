<template>
  <div>
    <Card>
      <template #header>
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-2">
            <UsersIcon class="h-6 w-6" />
            <h1 class="text-2xl font-bold">Gestão de Usuários</h1>
          </div>
        </div>
      </template>

      <!-- Loading/Error/Empty States -->
      <div v-if="loading" class="text-center py-10">
        <p>Carregando usuários...</p>
      </div>
      <div v-else-if="error" class="text-center py-10 text-red-500">
        <p>Ocorreu um erro ao carregar os usuários: {{ error.message }}</p>
      </div>
      <div v-else-if="!dataLoaded" class="text-center py-10">
        <p>Clique no botão abaixo para carregar os usuários.</p>
        <Button @click="loadData" variant="primary" class="mt-4">Carregar Usuários</Button>
      </div>
      <div v-else-if="users.length === 0" class="text-center py-10 text-gray-500">
        <p>Nenhum usuário encontrado.</p>
      </div>

      <!-- Users Table -->
      <div v-else class="overflow-x-auto mt-4">
        <table class="min-w-full bg-white">
          <thead class="bg-gray-100">
            <tr>
              <th class="py-2 px-4 border-b text-left">Nome</th>
              <th class="py-2 px-4 border-b text-left">Email</th>
              <th class="py-2 px-4 border-b text-left">Lotação</th>
              <th class="py-2 px-4 border-b text-left">Perfil</th>
              <th class="py-2 px-4 border-b text-left">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="py-2 px-4 border-b">{{ user.displayName }}</td>
              <td class="py-2 px-4 border-b">{{ user.email }}</td>
              <td class="py-2 px-4 border-b">{{ user.lotacao }}</td>
              <td class="py-2 px-4 border-b">
                <span :class="getProfileBadgeClass(user.perfil)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ user.perfil }}
                </span>
              </td>
              <td class="py-2 px-4 border-b">
                <Button @click="openEditModal(user)" variant="secondary" size="sm">Editar</Button>
              </td>
            </tr>
          </tbody>
        </table>
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
          <Button type="button" @click="closeModal" variant="default">Cancelar</Button>
          <Button form="user-form" type="submit" variant="primary" :loading="isSubmitting">Salvar</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import * as z from 'zod';
import { useToast } from 'vue-toastification';
import { UsersIcon } from '@heroicons/vue/24/outline';

import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';

type UserProfile = {
  id: string;
  displayName: string;
  email: string;
  lotacao: string;
  perfil: 'Trabalhador' | 'Chefia' | 'UDP';
};

const toast = useToast();

const users = ref<UserProfile[]>([]);
const loading = ref(false);
const error = ref<Error | null>(null);
const dataLoaded = ref(false);
const isModalOpen = ref(false);
const isSubmitting = ref(false);
const editingUser = ref<UserProfile | null>(null);

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

const fetchUsers = async () => {
  try {
    loading.value = true;
    const { data } = await api.get('/api/admin/usuarios');
    users.value = data.map((user: any) => ({
      ...user,
      displayName: user.nome,
    }));
    dataLoaded.value = true;
  } catch (err: any) {
    error.value = err;
    toast.error('Falha ao carregar os usuários.');
  } finally {
    loading.value = false;
  }
};

const loadData = () => {
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
      new_perfil: values.perfil,
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

const getProfileBadgeClass = (profile: string) => {
  switch (profile) {
    case 'UDP':
      return 'bg-red-100 text-red-800';
    case 'Chefia':
      return 'bg-yellow-100 text-yellow-800';
    case 'Trabalhador':
    default:
      return 'bg-blue-100 text-blue-800';
  }
};
</script>
