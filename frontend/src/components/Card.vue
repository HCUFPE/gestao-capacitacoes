<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="p-4 border-b border-white/10">
      <slot name="header"></slot>
    </div>
    <div class="p-6">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="p-4 border-t border-white/10">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'default', // 'default' ou 'primary'
  },
});

const cardClasses = computed(() => {
  if (props.variant === 'primary') {
    return 'bg-paper-primary text-white rounded-lg';
  }
  return 'bg-white shadow-paper rounded-lg';
});
</script>
