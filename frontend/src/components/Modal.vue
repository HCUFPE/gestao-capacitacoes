<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="show" 
           class="fixed inset-0 z-40" 
           style="background-color: rgba(0, 0, 0, 0.25); backdrop-filter: blur(4px);"
           @click="close"></div>
    </transition>
    <transition name="slide-up">
      <div v-if="show" class="fixed bottom-0 inset-x-0 sm:inset-0 sm:flex sm:items-center sm:justify-center z-50">
        <div :class="['bg-white rounded-t-lg sm:rounded-lg shadow-xl w-full m-4', maxWidthClass]">
          <div class="p-4 border-b flex justify-between items-center">
            <h2 class="text-xl font-semibold">
              <slot name="header">Modal Title</slot>
            </h2>
            <button @click="close" class="text-gray-500 hover:text-gray-700">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="p-4 overflow-y-auto max-h-[80vh]">
            <slot></slot>
          </div>
          <div v-if="$slots.footer" class="p-4 border-t flex justify-end space-x-4">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  size: {
    type: String,
    default: 'lg', // sm, md, lg, xl, 2xl, 3xl, 4xl, 5xl, 6xl, 7xl, full
  }
});

const maxWidthClass = computed(() => {
  switch (props.size) {
    case 'sm': return 'max-w-sm';
    case 'md': return 'max-w-md';
    case 'lg': return 'max-w-lg';
    case 'xl': return 'max-w-xl';
    case '2xl': return 'max-w-2xl';
    case '3xl': return 'max-w-3xl';
    case '4xl': return 'max-w-4xl';
    case '5xl': return 'max-w-5xl';
    case '6xl': return 'max-w-6xl';
    case '7xl': return 'max-w-7xl';
    case 'full': return 'max-w-full';
    default: return 'max-w-lg';
  }
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};

const handleEscape = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.show) {
    close();
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleEscape);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape);
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}

@media (min-width: 640px) {
  .slide-up-enter-from,
  .slide-up-leave-to {
    transform: translateY(0) scale(0.95);
    opacity: 0;
  }
  .slide-up-enter-active,
  .slide-up-leave-active {
    transition: all 0.3s ease;
  }
}
</style>
