import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import MeusCursos from './MeusCursos.vue';

vi.mock('../services/api', () => ({
  default: {
    get: vi.fn((url: string) => {
      if (url === '/api/atribuicoes/me') {
        return Promise.resolve({ data: [] });
      }
      if (url === '/api/inscricoes/me') {
        return Promise.resolve({
          data: [
            {
              id: 'inscricao-1',
              status: 'Em Andamento',
              atribuicao_id: 'atrib-1',
              curso: { id: 'curso-1', titulo: 'Curso Em Andamento', carga_horaria: 20 },
            },
            {
              id: 'inscricao-2',
              status: 'Realizado',
              atribuicao_id: 'atrib-2',
              curso: { id: 'curso-2', titulo: 'Curso Realizado', carga_horaria: 40 },
            },
          ],
        });
      }
      if (url === '/api/cursos/recommended' || url === '/api/cursos/genericos') {
        return Promise.resolve({ data: [] });
      }
      return Promise.resolve({ data: [] });
    }),
    post: vi.fn(),
    delete: vi.fn(),
  },
}));

vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn(),
  }),
}));

describe('MeusCursos.vue', () => {
  it('exibe o botão Desinscrever-se apenas para inscrições com status Em Andamento', async () => {
    const wrapper = mount(MeusCursos, {
      global: {
        stubs: {
          Card: { template: '<div><slot name="header"></slot><slot></slot></div>' },
          Button: { template: '<button><slot name="icon"></slot><slot></slot></button>' },
          CourseCard: { template: '<div><slot></slot><slot name="secondary-action"></slot><slot name="primary-action"></slot></div>' },
          CertificateUploadModal: true,
          CourseDetailsModal: true,
          CourseCatalogModal: true,
        },
      },
    });

    await flushPromises();

    const buttons = wrapper.findAll('button');
    const buttonTexts = buttons.map((b) => b.text());

    // Deve haver 1 botão de Desinscrever-se para a inscrição "Em Andamento", mas NÃO para a "Realizado"
    const unenrollCount = buttonTexts.filter((t) => t.includes('Desinscrever-se')).length;
    expect(unenrollCount).toBe(1);
  });
});
