import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import UserDetailsModal from '../components/UserDetailsModal.vue';

// Mock api
const mockApiGet = vi.fn();
vi.mock('../services/api', () => ({
  default: {
    get: (...args: any[]) => mockApiGet(...args),
  },
}));

// Enable teleport to body in jsdom
beforeEach(() => {
  document.body.innerHTML = '<div id="app"></div>';
});

describe('UserDetailsModal', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('não renderiza conteúdo quando show=false', async () => {
    mockApiGet.mockResolvedValue({ data: [] });

    const wrapper = mount(UserDetailsModal, {
      props: {
        show: false,
        userId: 'user-1',
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    await flushPromises();
    // The Modal uses teleport + v-if, so content should not be present
    expect(document.body.textContent).not.toContain('Detalhes do Usuário');
    // show=false should not trigger API call (watch only fires on change to true)
    expect(mockApiGet).not.toHaveBeenCalled();
  });

  it('chama API e exibe cursos quando show=true', async () => {
    mockApiGet.mockResolvedValue({
      data: [
        {
          id: 'attr-1',
          curso: { titulo: 'Curso A', certificadora: 'Plataforma X', carga_horaria: 20, ano_gd: '2025' },
          status: 'Validado',
          certificado_file_path: null,
          certificado_link: null,
        },
        {
          id: 'attr-2',
          curso: { titulo: 'Curso B', certificadora: 'Plataforma Y', carga_horaria: 40, ano_gd: '2024' },
          status: 'Realizado',
          certificado_file_path: 'cert1.pdf',
          certificado_link: null,
        },
      ],
    });

    const wrapper = mount(UserDetailsModal, {
      props: {
        show: true,
        userId: 'user-1',
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();

    expect(mockApiGet).toHaveBeenCalledWith('/api/relatorios/usuario/user-1/detalhes');

    // Check teleported content in body - data is flattened by computed
    const bodyContent = document.body.textContent!;
    expect(bodyContent).toContain('Curso A');
    expect(bodyContent).toContain('Curso B');
    expect(bodyContent).toContain('Plataforma X');
    expect(bodyContent).toContain('Validado');
    expect(bodyContent).toContain('Realizado');
  });

  it('exibe mensagem de erro quando API falha', async () => {
    mockApiGet.mockRejectedValue({
      response: { data: { detail: 'Usuário não encontrado.' } },
    });

    const wrapper = mount(UserDetailsModal, {
      props: {
        show: true,
        userId: 'user-invalid',
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();

    expect(document.body.textContent).toContain('Erro ao carregar detalhes');
  });

  it('emite evento close ao clicar no botão Fechar', async () => {
    mockApiGet.mockResolvedValue({ data: [] });

    const wrapper = mount(UserDetailsModal, {
      props: {
        show: true,
        userId: 'user-1',
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();

    // Find the button with text "Fechar" in the teleported content
    const buttons = Array.from(document.querySelectorAll('button'));
    let closeButton: HTMLButtonElement | null = null;
    for (const btn of buttons) {
      if (btn.textContent?.includes('Fechar')) {
        closeButton = btn as HTMLButtonElement;
        break;
      }
    }
    expect(closeButton).not.toBeNull();

    if (closeButton) {
      closeButton.click();
      await flushPromises();
    }

    expect(wrapper.emitted('close')).toBeDefined();
  });

  it('exibe link de certificado quando certificado_link está presente', async () => {
    mockApiGet.mockResolvedValue({
      data: [
        {
          id: 'attr-1',
          curso: { titulo: 'Curso Cert', certificadora: 'Plat', carga_horaria: 10, ano_gd: '2025' },
          status: 'Validado',
          certificado_file_path: null,
          certificado_link: 'https://example.com/cert.pdf',
        },
      ],
    });

    const wrapper = mount(UserDetailsModal, {
      props: {
        show: true,
        userId: 'user-1',
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();

    // Check that the certificate link text appears in the body
    const bodyContent = document.body.textContent!;
    expect(bodyContent).toContain('Visualizar');
    // Check that the <a> element has the correct href
    const links = document.querySelectorAll('a[href]');
    const certLink = Array.from(links).find(a => a.textContent?.includes('Visualizar')) as HTMLAnchorElement | undefined;
    expect(certLink).toBeDefined();
    if (certLink) {
      expect(certLink.getAttribute('href')).toBe('https://example.com/cert.pdf');
    }
  });

  it('carrega dados novamente quando show muda para true', async () => {
    mockApiGet.mockResolvedValue({ data: [] });

    const wrapper = mount(UserDetailsModal, {
      props: {
        show: false,
        userId: 'user-1',
      },
      global: {
        stubs: {
          teleport: false,
        },
      },
    });

    // With immediate:true on watch, show=false should not trigger fetch
    await flushPromises();
    expect(mockApiGet).not.toHaveBeenCalled();

    await wrapper.setProps({ show: true });
    await flushPromises();

    expect(mockApiGet).toHaveBeenCalledWith('/api/relatorios/usuario/user-1/detalhes');
  });
});
