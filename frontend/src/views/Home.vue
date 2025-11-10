<template>
  <Card>
    <template #header>
      <div class="flex items-center space-x-2">
        <HomeIcon class="h-6 w-6" />
        <h1 class="text-2xl font-bold">Bem-vindo ao Portal de Capacitações EAD!</h1>
      </div>
    </template>
    <p class="mt-4 text-paper-text">
      Esta plataforma foi desenvolvida para centralizar o gerenciamento de capacitações EAD,
      facilitando o processo de definição, execução e validação de cursos para fins de Gestão de Desempenho (GD).
    </p>
    <p class="mt-2 text-paper-text">
      Aqui você poderá acompanhar seus cursos atribuídos, registrar certificados e, se for uma chefia,
      gerenciar as capacitações da sua equipe.
    </p>
    <div class="mt-6">
      <router-link v-if="authStore.isAuthenticated" to="/meus-cursos">
        <Button variant="primary">Ver Meus Cursos</Button>
      </router-link>
      <router-link v-else to="/login">
        <Button variant="primary">Fazer Login</Button>
      </router-link>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import { useAuthStore } from '../stores/auth';
import { HomeIcon } from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
</script>
