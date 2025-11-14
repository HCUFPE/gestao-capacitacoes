<template>
  <Modal :show="show" @close="$emit('close')">
    <template #header>
      <h2 class="text-xl font-semibold">Enviar Certificado</h2>
    </template>
    
    <div class="mt-4">
      <div v-if="!file">
        <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
          <span>Selecione um arquivo</span>
          <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="handleFileChange">
        </label>
        <p class="text-xs text-gray-500 mt-1">PDF, PNG, JPG ou GIF até 10MB</p>
      </div>
      <div v-else>
        <p class="text-sm font-medium text-gray-900">Arquivo selecionado:</p>
        <div class="mt-2 flex items-center justify-between">
          <span class="text-sm text-gray-700">{{ file.name }}</span>
          <button @click="file = null" class="text-red-600 hover:text-red-800">
            <XCircleIcon class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-4">
        <Button type="button" @click="$emit('close')" variant="default">Cancelar</Button>
        <Button type="button" @click="handleUpload" variant="primary" :disabled="!file || isUploading" :loading="isUploading">
          <template #icon><ArrowUpTrayIcon class="h-5 w-5" /></template>
          Enviar
        </Button>
      </div>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useToast } from 'vue-toastification';
import { XCircleIcon, ArrowUpTrayIcon } from '@heroicons/vue/24/outline';
import Modal from './Modal.vue';
import Button from './Button.vue';
import api from '../services/api';

const props = defineProps<{
  show: boolean;
  atribuicaoId: string | null;
}>();

const emit = defineEmits(['close', 'upload-success']);

const file = ref<File | null>(null);
const isUploading = ref(false);
const toast = useToast();

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    file.value = target.files[0];
  }
};

const handleUpload = async () => {
  if (!file.value || !props.atribuicaoId) return;

  isUploading.value = true;
  try {
    const formData = new FormData();
    formData.append('file', file.value);
    formData.append('atribuicao_id', props.atribuicaoId);

    await api.post('/api/certificados/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    toast.success('Certificado enviado com sucesso!');
    emit('upload-success');
  } catch (err: any) {
    toast.error(`Erro ao enviar o certificado: ${err.response?.data?.detail || err.message}`);
  } finally {
    isUploading.value = false;
  }
};
</script>
