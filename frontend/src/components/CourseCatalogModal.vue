<template>
  <Modal :show="show" @close="close" size="4xl">
    <template #header>Catálogo de Cursos</template>

    <div class="space-y-4">
      <!-- Search Bar -->
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </div>
        <input
          v-model="searchQuery"
          type="text"
          class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          placeholder="Buscar cursos por título, tema ou palavra-chave..."
        />
      </div>

      <!-- Course List -->
      <div v-if="paginatedCourses.length > 0" class="space-y-2 max-h-[60vh] overflow-y-auto">
        <div v-for="curso in paginatedCourses" :key="curso.id" class="p-4 border rounded-lg hover:shadow-md transition-shadow duration-200 bg-white flex justify-between items-center">
          <div>
            <h3 class="text-lg font-medium text-gray-900">{{ curso.titulo }}</h3>
            <div class="flex items-center space-x-4 mt-1 text-sm text-gray-500">
              <span v-if="curso.tema" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {{ curso.tema }}
              </span>
              <span>{{ curso.carga_horaria ? curso.carga_horaria + 'h' : '' }}</span>
              <span v-if="curso.certificadora">{{ curso.certificadora }}</span>
            </div>
          </div>
          <Button @click="enroll(curso.id)" variant="success" size="sm" class="flex-shrink-0 ml-4">
            <template #icon><PlusCircleIcon class="h-4 w-4" /></template>
            Inscrever-se
          </Button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-10">
        <p class="text-gray-500 text-lg">Nenhum curso encontrado.</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-gray-200 pt-4">
        <Button @click="prevPage" :disabled="currentPage === 1" variant="secondary" size="sm">
          Anterior
        </Button>
        <span class="text-sm text-gray-700">
          Página <span class="font-medium">{{ currentPage }}</span> de <span class="font-medium">{{ totalPages }}</span>
        </span>
        <Button @click="nextPage" :disabled="currentPage === totalPages" variant="secondary" size="sm">
          Próximo
        </Button>
      </div>
    </div>

    <template #footer>
      <Button @click="close" variant="secondary">Fechar</Button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import Modal from './Modal.vue';
import Button from './Button.vue';
import { MagnifyingGlassIcon, PlusCircleIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
  show: Boolean,
  courses: {
    type: Array as () => any[],
    default: () => [],
  },
});

const emit = defineEmits(['close', 'enroll']);

const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 5;

// Filter courses based on search query
const filteredCourses = computed(() => {
  if (!searchQuery.value) {
    return props.courses;
  }
  const query = searchQuery.value.toLowerCase();
  return props.courses.filter((curso) => 
    (curso.titulo && curso.titulo.toLowerCase().includes(query)) ||
    (curso.tema && curso.tema.toLowerCase().includes(query))
  );
});

// Calculate total pages
const totalPages = computed(() => {
  return Math.ceil(filteredCourses.value.length / itemsPerPage);
});

// Get items for current page
const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredCourses.value.slice(start, end);
});

// Reset to page 1 when search query changes
watch(searchQuery, () => {
  currentPage.value = 1;
});

const close = () => {
  emit('close');
};

const enroll = (cursoId: string) => {
  emit('enroll', cursoId);
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};
</script>