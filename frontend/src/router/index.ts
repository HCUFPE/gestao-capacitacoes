import { createRouter, createWebHistory, NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import MeusCursos from '../views/MeusCursos.vue';
import GestaoCursos from '../views/GestaoCursos.vue';
import GestaoUsuarios from '../views/GestaoUsuarios.vue';
import RelatoriosUdp from '../views/RelatoriosUdp.vue';
import RelatoriosChefia from '../views/RelatoriosChefia.vue';
import RelatoriosCapacitacoes from '../views/RelatoriosCapacitacoes.vue';
import ValidacaoCertificados from '../views/ValidacaoCertificados.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { layout: 'LoginLayout' },
  },
  {
    path: '/meus-cursos',
    name: 'Meus Cursos',
    component: MeusCursos,
    meta: { requiresAuth: true },
  },
  {
    path: '/gestao-cursos',
    name: 'Gestão de Cursos',
    component: GestaoCursos,
    meta: { requiresAuth: true, requiresProfile: ['Chefia', 'UDP'] },
  },
  {
    path: '/gestao-usuarios',
    name: 'Gestão de Usuários',
    component: GestaoUsuarios,
    meta: { requiresAuth: true, requiresProfile: 'UDP' },
  },
  {
    path: '/relatorios/udp',
    name: 'Relatórios UDP',
    component: RelatoriosUdp,
    meta: { requiresAuth: true, requiresProfile: 'UDP' },
  },
  {
    path: '/relatorios/capacitacoes',
    name: 'Relatórios Capacitações',
    component: RelatoriosCapacitacoes,
    meta: { requiresAuth: true, requiresProfile: 'UDP' },
  },
  {
    path: '/relatorios/chefia',
    name: 'Relatórios Chefia',
    component: RelatoriosChefia,
    meta: { requiresAuth: true, requiresProfile: ['Chefia', 'UDP'] },
  },
  {
    path: '/validacao-certificados',
    name: 'Validação de Certificados',
    component: ValidacaoCertificados,
    meta: { requiresAuth: true, requiresProfile: ['Chefia', 'UDP'] },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: 'bg-paper-active-link',
  linkExactActiveClass: 'bg-paper-active-link',
});

router.beforeEach((to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
  const authStore = useAuthStore();

  if (to.name === 'Login' && authStore.isAuthenticated) {
    return next({ name: 'Meus Cursos' });
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'Login' });
  }

  if (to.meta.requiresProfile && authStore.isAuthenticated) {
    const requiredProfiles = Array.isArray(to.meta.requiresProfile)
      ? to.meta.requiresProfile
      : [to.meta.requiresProfile];
    
    const userProfile = authStore.user?.perfil;

    if (!userProfile || !requiredProfiles.includes(userProfile)) {
      console.warn(`Acesso negado à rota ${to.path}. Perfil necessário: ${requiredProfiles.join(' ou ')}. Perfil do usuário: ${userProfile}`);
      return next({ name: 'Home' });
    }
  }

  next();
});

export default router;
