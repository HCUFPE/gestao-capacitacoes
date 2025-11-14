<template>
  <div class="max-w-full mx-auto p-4 border border-gray-200 rounded-lg bg-gray-50">
    <div class="md:flex">
      <div class="md:flex-shrink-0">
        <div class="h-32 w-full md:w-32 bg-gray-200 flex items-center justify-center">
          <AcademicCapIcon class="h-16 w-16 text-gray-400" />
        </div>
      </div>
      <div class="p-4 flex-grow">
        <div class="flex items-center">
          <a :href="curso.link" target="_blank" rel="noopener noreferrer" class="block text-lg leading-tight font-medium text-black hover:underline">{{ curso.titulo }}</a>
          <a v-if="curso.link" :href="curso.link" target="_blank" rel="noopener noreferrer" class="ml-2 text-blue-500 hover:text-blue-700">
            <LinkIcon class="h-5 w-5" />
          </a>
        </div>
        <div class="flex items-center text-sm text-gray-500 mt-1">
          <span class="uppercase tracking-wide text-indigo-500 font-semibold mr-2">{{ curso.ano_gd }}</span>
          <span>Carga Horária: {{ curso.carga_horaria }}h</span>
        </div>
        <div class="mt-2">
          <span v-if="curso.status" class="px-3 py-1 text-sm font-semibold rounded-full" :class="getStatusClass(curso.status)">
            {{ curso.status }}
          </span>
          <div class="flex justify-end space-x-2 mt-2">
            <slot name="secondary-action"></slot>
            <slot name="primary-action"></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AcademicCapIcon, LinkIcon } from '@heroicons/vue/24/outline';

defineProps<{
  curso: {
    id: string;
    titulo: string;
    carga_horaria: number;
    ano_gd: string;
    link?: string;
    status?: string;
    atribuicaoId?: string; // New prop for assignment ID
  };
}>();

defineEmits(['send-certificate']); // Define the custom event

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
</script>
