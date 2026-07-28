<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Importar Cursos (CSV)</h3>
        <button @click="close" class="text-gray-500 hover:text-gray-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <div v-if="!resultado" class="space-y-4">
        <p class="text-sm text-gray-600">Selecione o arquivo CSV contendo os dados dos cursos (delimitador ponto e vírgula, encoding UTF-8 ou ISO-8859-1).</p>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Arquivo CSV</label>
          <input 
            type="file" 
            accept=".csv" 
            @change="onFileChange"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <div v-if="errorMsg" class="p-3 bg-red-100 text-red-700 rounded-md text-sm whitespace-pre-line">
          {{ errorMsg }}
        </div>

        <div class="flex justify-end space-x-3 mt-6">
          <button @click="close" class="px-4 py-2 border rounded-md text-gray-600 hover:bg-gray-50" :disabled="isLoading">
            Cancelar
          </button>
          <button @click="importar" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center" :disabled="!selectedFile || isLoading">
            <span v-if="isLoading" class="mr-2">
              <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            Importar
          </button>
        </div>
      </div>

      <div v-else class="space-y-4">
        <div class="p-4 bg-green-50 border border-green-200 rounded-md">
          <h4 class="text-green-800 font-medium mb-2">Importação Concluída</h4>
          <ul class="list-disc pl-5 text-sm text-green-700 space-y-1">
            <li><strong>{{ resultado.novos }}</strong> novos cursos cadastrados</li>
            <li><strong>{{ resultado.atualizados }}</strong> cursos atualizados</li>
          </ul>
        </div>
        
        <div v-if="resultado.erros && resultado.erros.length > 0" class="mt-4">
          <h4 class="text-sm font-semibold text-red-800 mb-2">Avisos / Erros:</h4>
          <div class="max-h-40 overflow-y-auto p-3 bg-red-50 text-red-700 rounded-md text-xs whitespace-pre-line border border-red-200">
            <div v-for="(err, index) in resultado.erros" :key="index">{{ err }}</div>
          </div>
        </div>

        <div class="flex justify-end mt-6">
          <button @click="fecharEAtualizar" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Concluir
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { importarCursosCsv } from '../services/cursoService';
import type { AxiosError } from 'axios';

const props = defineProps({
  show: Boolean
});

const emit = defineEmits(['close', 'imported']);

const selectedFile = ref<File | null>(null);
const isLoading = ref(false);
const errorMsg = ref('');
const resultado = ref<any>(null);

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0];
    errorMsg.value = '';
  }
};

const close = () => {
  resetState();
  emit('close');
};

const resetState = () => {
  selectedFile.value = null;
  isLoading.value = false;
  errorMsg.value = '';
  resultado.value = null;
};

const fecharEAtualizar = () => {
  emit('imported');
  close();
};

const importar = async () => {
  if (!selectedFile.value) return;
  
  isLoading.value = true;
  errorMsg.value = '';
  
  try {
    const res = await importarCursosCsv(selectedFile.value);
    resultado.value = res;
  } catch (err: any) {
    const axiosError = err as AxiosError<any>;
    errorMsg.value = axiosError.response?.data?.detail || err.message || 'Erro desconhecido ao importar.';
  } finally {
    isLoading.value = false;
  }
};
</script>
