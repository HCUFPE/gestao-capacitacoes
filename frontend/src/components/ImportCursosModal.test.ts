import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import ImportCursosModal from './ImportCursosModal.vue';
import * as cursoService from '../services/cursoService';

// Mock course service
vi.mock('../services/cursoService', () => ({
  importarCursosCsv: vi.fn(),
}));

// Enable teleport to body in jsdom
beforeEach(() => {
  document.body.innerHTML = '<div id="app"></div>';
  vi.clearAllMocks();
});

describe('ImportCursosModal', () => {
  it('não renderiza o modal quando show=false', async () => {
    const wrapper = mount(ImportCursosModal, {
      props: { show: false },
    });
    await flushPromises();
    expect(wrapper.find('h3').exists()).toBe(false);
  });

  it('exibe o formulário inicial quando show=true', async () => {
    const wrapper = mount(ImportCursosModal, {
      props: { show: true },
    });
    await flushPromises();
    
    expect(wrapper.find('h3').text()).toBe('Importar Cursos (CSV)');
    expect(wrapper.find('input[type="file"]').exists()).toBe(true);
    expect(wrapper.find('button').text()).not.toContain('Importação Concluída');
  });

  it('permite selecionar um arquivo', async () => {
    const wrapper = mount(ImportCursosModal, {
      props: { show: true },
    });
    
    const file = new File(['csv content'], 'cursos.csv', { type: 'text/csv' });
    const input = wrapper.find('input[type="file"]');
    
    // Simulate file selection using HTMLInputElement properties
    Object.defineProperty(input.element, 'files', {
      value: [file]
    });
    await input.trigger('change');
    
    // Check that button is no longer disabled (if it was)
    const importarBtn = wrapper.findAll('button').find(b => b.text().includes('Importar'));
    expect(importarBtn?.attributes('disabled')).toBeUndefined();
  });

  it('exibe resultado após importação bem-sucedida', async () => {
    (cursoService.importarCursosCsv as any).mockResolvedValue({
      novos: 5,
      atualizados: 2,
      erros: []
    });

    const wrapper = mount(ImportCursosModal, {
      props: { show: true },
    });
    
    // Simulate file selection
    const file = new File(['csv content'], 'cursos.csv', { type: 'text/csv' });
    const input = wrapper.find('input[type="file"]');
    Object.defineProperty(input.element, 'files', { value: [file] });
    await input.trigger('change');
    
    // Click import
    const importarBtn = wrapper.findAll('button').find(b => b.text().includes('Importar'));
    await importarBtn?.trigger('click');
    await flushPromises();
    
    // Check results
    expect(cursoService.importarCursosCsv).toHaveBeenCalledWith(file);
    expect(wrapper.text()).toContain('Importação Concluída');
    expect(wrapper.text()).toContain('5 novos cursos cadastrados');
    expect(wrapper.text()).toContain('2 cursos atualizados');
  });

  it('exibe erros se a importação falhar', async () => {
    (cursoService.importarCursosCsv as any).mockRejectedValue({
      response: { data: { detail: 'Erro de formato CSV' } }
    });

    const wrapper = mount(ImportCursosModal, {
      props: { show: true },
    });
    
    // Simulate file selection
    const file = new File(['bad content'], 'bad.csv', { type: 'text/csv' });
    const input = wrapper.find('input[type="file"]');
    Object.defineProperty(input.element, 'files', { value: [file] });
    await input.trigger('change');
    
    // Click import
    const importarBtn = wrapper.findAll('button').find(b => b.text().includes('Importar'));
    await importarBtn?.trigger('click');
    await flushPromises();
    
    // Check error message
    expect(wrapper.text()).toContain('Erro de formato CSV');
  });
});
