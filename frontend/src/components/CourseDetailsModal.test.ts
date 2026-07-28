import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import CourseDetailsModal from './CourseDetailsModal.vue';

// Mock getCertificateUrl to keep tests simple
vi.mock('../services/certificateUtils', () => ({
  getCertificateUrl: (item: any) => {
    if (item.certificado_link) return item.certificado_link;
    if (item.certificado_file_path) return `/api/certificados/download/${item.certificado_file_path}`;
    return null;
  },
}));

beforeEach(() => {
  document.body.innerHTML = '<div id="app"></div>';
});

describe('CourseDetailsModal', () => {
  const getCursoMock = (status: string, hasCert = true) => ({
    id: 'curso-1',
    titulo: 'Curso de Teste',
    carga_horaria: 40,
    ano_gd: '2025',
    status,
    atribuicaoId: 'atrib-1',
    certificado_id: hasCert ? 'cert-1' : undefined,
    certificado_file_path: hasCert ? 'cert1.pdf' : undefined,
  });

  it('exibe botão "Reenviar Certificado" quando status é Recusado e possui certificado', () => {
    const wrapper = mount(CourseDetailsModal, {
      props: {
        show: true,
        curso: getCursoMock('Recusado'),
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    // In jsdom/teleport, we can look at document.body or wrapper.html
    const html = document.body.innerHTML;
    expect(html).toContain('Reenviar Certificado');
    expect(html).not.toContain('Enviar Certificado');
  });

  it('exibe botão "Reenviar Certificado" quando status é Realizado e possui certificado', () => {
    mount(CourseDetailsModal, {
      props: {
        show: true,
        curso: getCursoMock('Realizado'),
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    const html = document.body.innerHTML;
    expect(html).toContain('Reenviar Certificado');
    expect(html).not.toContain('Enviar Certificado');
  });

  it('NÃO exibe botão "Reenviar Certificado" quando status é Validado ou Concluído', () => {
    mount(CourseDetailsModal, {
      props: {
        show: true,
        curso: getCursoMock('Validado'),
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    const html = document.body.innerHTML;
    expect(html).not.toContain('Reenviar Certificado');
  });

  it('exibe botão "Enviar Certificado" quando status é Em Andamento', () => {
    mount(CourseDetailsModal, {
      props: {
        show: true,
        curso: getCursoMock('Em Andamento', false),
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    const html = document.body.innerHTML;
    expect(html).toContain('Enviar Certificado');
    expect(html).not.toContain('Reenviar Certificado');
  });
});
