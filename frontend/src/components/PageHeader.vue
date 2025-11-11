<template>
  <div class="flex justify-between items-center">
    <div class="flex items-center space-x-2">
      <component :is="icon" class="h-6 w-6" v-if="icon" />
      <h1 class="text-2xl font-bold">{{ title }}</h1>
    </div>
    <div v-if="$slots.actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

defineProps({
  title: {
    type: String,
    required: true,
  },
  icon: {
    type: Object, // Expecting a Vue component for the icon
    default: null,
  },
});
</script>
