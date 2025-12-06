<template>
  <div class="bg-white p-6 rounded-lg shadow-md border border-gray-100 flex items-start space-x-4 h-full">
    <div class="flex-shrink-0 h-12 w-12 rounded-full flex items-center justify-center" :class="iconBgColor">
      <component :is="item.icon" class="h-6 w-6" :class="item.color" aria-hidden="true" />
    </div>
    <div>
      <p class="text-3xl font-bold text-gray-800">{{ item.value }}</p>
      <p class="text-sm font-medium text-gray-500 truncate">{{ item.name }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, PropType } from 'vue';

interface StatItem {
  name: string;
  value: number | string;
  icon: any;
  color: string;
}

const props = defineProps({
  item: {
    type: Object as PropType<StatItem>,
    required: true,
  },
});

const iconBgColor = computed(() => {
  const color = props.item.color || 'text-gray-500';
  if (color.includes('blue')) return 'bg-blue-100';
  if (color.includes('indigo')) return 'bg-indigo-100';
  if (color.includes('green')) return 'bg-green-100';
  if (color.includes('yellow')) return 'bg-yellow-100';
  if (color.includes('cyan')) return 'bg-cyan-100';
  if (color.includes('red')) return 'bg-red-100';
  return 'bg-gray-100';
});
</script>
