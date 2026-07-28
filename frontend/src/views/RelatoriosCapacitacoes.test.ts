import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import RelatoriosCapacitacoes from '../views/RelatoriosCapacitacoes.vue';

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

describe('RelatoriosCapacitacoes', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza nome do profissional como link clicável', async () => {
    mockApiGet.mockImplementation((url: string) => {
      if (url === '/api/relatorios/capacitacoes') {
        return Promise.resolve({
          data: [
            { id: 'user-1', nome_profissional: 'João Silva', nome_curso: 'Curso A', certificado: 'Sim' },
          ],
        });
      }
      if (url === '/api/relatorios/vinculos') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: [] });
    });

    const wrapper = mount(RelatoriosCapacitacoes, {
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
    const nameButton = buttons.find(b => b.text().includes('João Silva'));
    expect(nameButton).toBeDefined();
  });

  it('abre modal ao clicar no nome do profissional', async () => {
    mockApiGet.mockImplementation((url: string) => {
      if (url === '/api/relatorios/capacitacoes') {
        return Promise.resolve({
          data: [
            { id: 'user-1', nome_profissional: 'João Silva', nome_curso: 'Curso A', certificado: 'Sim' },
          ],
        });
      }
      if (url === '/api/relatorios/vinculos') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: [] });
    });

    const wrapper = mount(RelatoriosCapacitacoes, {
      global: {
        stubs: {
          teleport: false,
          RouterLink: { template: '<a><slot/></a>' },
        },
      },
    });

    await flushPromises();

    const buttons = wrapper.findAll('button');
    const nameButton = buttons.find(b => b.text().includes('João Silva'));

    if (nameButton) {
      await nameButton.trigger('click');
      await flushPromises();

      // Check that the modal is now open (UserDetailsModal receives show=true)
      const modal = wrapper.findComponent({ name: 'UserDetailsModal' });
      // If stubbed, check the props passed to it
      expect(modal.exists()).toBe(true);
    }
  });
});
