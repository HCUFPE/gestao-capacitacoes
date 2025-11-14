<template>
  <div class="flex justify-between items-center mt-4">
    <Button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" variant="default" size="sm">
      <template #icon><ChevronLeftIcon class="h-5 w-5" /></template>
      Anterior
    </Button>
    <span class="text-sm text-gray-700">
      Página <span class="font-semibold">{{ currentPage }}</span> de <span class="font-semibold">{{ totalPages }}</span> (Total: {{ totalItems }} itens)
    </span>
    <Button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages || totalPages === 0" variant="default" size="sm">
      Próxima
      <template #icon><ChevronRightIcon class="h-5 w-5" /></template>
    </Button>
  </div>
</template>

<script setup lang="ts">
import Button from './Button.vue';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  totalItems: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['update:currentPage']);

const changePage = (page: number) => {
  if (page > 0 && page <= props.totalPages) {
    emit('update:currentPage', page);
  }
};
</script>
