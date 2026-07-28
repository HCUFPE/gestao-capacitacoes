import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import RelatorioConsolidado from '../views/RelatorioConsolidado.vue';

// Mock api
const mockApiGet = vi.fn();
vi.mock('../services/api', () => ({
  default: {
    get: (...args: any[]) => mockApiGet(...args),
    create: vi.fn(() => ({
      get: mockApiGet,
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    })),
  },
}));

// Mock vue-router
vi.mock('vue-router', () => ({
  useRoute: () => ({ query: {}, meta: { role: 'UDP' } }),
}));

describe('RelatorioConsolidado', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza nome como link clicável', async () => {
    mockApiGet.mockImplementation((url: string) => {
      if (url.includes('/consolidado')) {
        return Promise.resolve({
          data: [
            { id: 'user-1', nome: 'Maria Santos', nome_curso: 'Curso B', status: 'Validado', certificado_enviado: 'Sim' },
          ],
        });
      }
      if (url === '/api/relatorios/vinculos') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: [] });
    });

    const wrapper = mount(RelatorioConsolidado, {
      global: {
        stubs: {
          teleport: false,
          RouterLink: { template: '<a><slot/></a>' },
        },
      },
    });

    await flushPromises();

    // Find the button with the user's name
    const buttons = wrapper.findAll('button');
    const nameButton = buttons.find(b => b.text().includes('Maria Santos'));
    expect(nameButton).toBeDefined();
  });

  it('abre modal de detalhes ao clicar no nome', async () => {
    mockApiGet.mockImplementation((url: string) => {
      if (url.includes('/consolidado')) {
        return Promise.resolve({
          data: [
            { id: 'user-2', nome: 'Carlos Oliveira', nome_curso: 'Curso C', status: 'Realizado', certificado_enviado: 'Não' },
          ],
        });
      }
      if (url === '/api/relatorios/vinculos') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: [] });
    });

    const wrapper = mount(RelatorioConsolidado, {
      global: {
        stubs: {
          teleport: false,
          RouterLink: { template: '<a><slot/></a>' },
        },
      },
    });

    await flushPromises();

    const buttons = wrapper.findAll('button');
    const nameButton = buttons.find(b => b.text().includes('Carlos Oliveira'));

    if (nameButton) {
      await nameButton.trigger('click');
      await flushPromises();

      const modal = wrapper.findComponent({ name: 'UserDetailsModal' });
      expect(modal.exists()).toBe(true);
    }
  });
});
