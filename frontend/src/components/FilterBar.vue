<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
    <!-- Dynamic Filter Inputs -->
    <div v-for="filter in filters" :key="filter.key" class="form-group">
      <label :for="`filter-${filter.key}`" class="form-label text-sm font-medium text-gray-700">{{ filter.label }}</label>
      <div class="relative">
        <div v-if="filter.icon" class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <component :is="filter.icon" class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </div>
        <input 
          type="text" 
          :id="`filter-${filter.key}`" 
          v-model="localFilterValues[filter.key]" 
          class="form-control"
          :class="{ 'pl-10': filter.icon }"
          :placeholder="filter.placeholder"
          @keyup.enter="apply"
        >
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex items-end space-x-2" :class="{'md:col-start-3': filters.length < 3}">
      <Button @click="apply" variant="primary" class="w-full md:w-auto">
        <template #icon><FunnelIcon class="h-5 w-5" /></template>
        Filtrar
      </Button>
      <Button @click="clear" variant="secondary" class="w-full md:w-auto">
        <template #icon><XCircleIcon class="h-5 w-5" /></template>
        Limpar
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, PropType } from 'vue';
import Button from './Button.vue';
import { FunnelIcon, XCircleIcon } from '@heroicons/vue/24/outline';

// Define the structure of a filter
interface Filter {
  key: string;
  label: string;
  placeholder: string;
  icon?: any; // Can be a component
}

const props = defineProps({
  filters: {
    type: Array as PropType<Filter[]>,
    required: true,
  },
});

const emit = defineEmits(['apply-filters', 'clear-filters']);

// Internal state for the filter values
const localFilterValues = ref<Record<string, string>>({});

// Initialize local state from props
props.filters.forEach(filter => {
  localFilterValues.value[filter.key] = '';
});

const apply = () => {
  emit('apply-filters', localFilterValues.value);
};

const clear = () => {
  Object.keys(localFilterValues.value).forEach(key => {
    localFilterValues.value[key] = '';
  });
  emit('clear-filters');
};
</script>
