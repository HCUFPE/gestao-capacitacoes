import { describe, it, expect, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import Home from './Home.vue';

vi.mock('../stores/auth', () => ({
  useAuthStore: () => ({
    user: { displayName: 'Usuário Teste' },
    isAuthenticated: true,
    isManagerOrAdmin: true,
  }),
}));

vi.mock('../services/api', () => ({
  default: {
    get: vi.fn(() =>
      Promise.resolve({
        data: {
          total_cursos: 15,
          total_inscricoes: 42,
          total_certificados_validados: 10,
          total_usuarios: 8,
          minhas_inscricoes: 3,
          meus_certificados_enviados: 2,
          meus_certificados_validados: 1,
        },
      })
    ),
  },
}));

describe('Home.vue', () => {
  it('renders personal and global stats sections correctly', async () => {
    const wrapper = mount(Home, {
      global: {
        stubs: {
          StatCard: {
            props: ['item'],
            template: '<div class="stat-card">{{ item.name }}: {{ item.value }}</div>',
          },
          Button: { template: '<button><slot name="icon"></slot><slot></slot></button>' },
          'router-link': { template: '<a><slot></slot></a>' },
        },
      },
    });

    await flushPromises();

    expect(wrapper.text()).toContain('Seu Panorama Pessoal');
    expect(wrapper.text()).toContain('Visão Geral do Sistema');

    const statCards = wrapper.findAll('.stat-card');
    // 3 personal stats + 4 global stats = 7 cards total
    expect(statCards.length).toBe(7);
    expect(wrapper.text()).toContain('Minhas Inscrições: 3');
    expect(wrapper.text()).toContain('Cursos Disponíveis: 15');
  });
});
