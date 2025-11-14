import { createRouter, createWebHistory, NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import MeusCursos from '../views/MeusCursos.vue';
import GestaoCursos from '../views/GestaoCursos.vue';
import GestaoUsuarios from '../views/GestaoUsuarios.vue';
import RelatoriosUdp from '../views/RelatoriosUdp.vue'; // Importar novo componente
import RelatoriosChefia from '../views/RelatoriosChefia.vue'; // Importar novo componente

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
    meta: { requiresAuth: true },
  },
  {
    path: '/gestao-usuarios',
    name: 'Gestão de Usuários',
    component: GestaoUsuarios,
    meta: { requiresAuth: true },
  },
  {
    path: '/relatorios/udp',
    name: 'Relatórios UDP',
    component: RelatoriosUdp,
    meta: { requiresAuth: true, requiresProfile: 'UDP' }, // Requer perfil UDP
  },
  {
    path: '/relatorios/chefia',
    name: 'Relatórios Chefia',
    component: RelatoriosChefia,
    meta: { requiresAuth: true, requiresProfile: 'Chefia' }, // Requer perfil Chefia
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

  // Se o usuário está autenticado e tenta acessar a página de login, redireciona para 'Meus Cursos'
  if (to.name === 'Login' && authStore.isAuthenticated) {
    next({ name: 'Meus Cursos' });
    return;
  }

  // Se a rota requer autenticação e o usuário não está autenticado, redireciona para 'Login'
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' });
    return;
  }

  // Se a rota requer um perfil específico e o usuário não tem esse perfil, redireciona para 'Home'
  if (to.meta.requiresProfile && authStore.isAuthenticated) {
    const requiredProfile = to.meta.requiresProfile as string;
    if (authStore.user?.profile !== requiredProfile) {
      next({ name: 'Home' }); // Redireciona para Home se o perfil não corresponder
      return;
    }
  }

  next();
});

export default router;
