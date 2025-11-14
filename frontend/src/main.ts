import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './index.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'; // 1. Importar o authStore

import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

// 2. Criar uma função async de inicialização
async function initializeApp() {
  const app = createApp(App);
  const pinia = createPinia();

  app.use(pinia);

  // 3. Inicializar o authStore ANTES de registrar o roteador
  const authStore = useAuthStore();
  await authStore.initializeAuth();

  app.use(router);
  app.use(Toast);

  // 4. Montar a aplicação
  app.mount('#app');
}

initializeApp();
