import { describe, it, expect } from 'vitest'
import { mount, config } from '@vue/test-utils'
import { nextTick } from 'vue'
import CourseDetailsModal from '../src/components/CourseDetailsModal.vue'

// Mock Modal and Button to render slots directly (avoids teleport/transition issues)
config.global.components = {
  Modal: {
    template: '<div><slot name="header" /><slot /><slot name="footer" /></div>',
    props: ['show', 'size'],
  },
  Button: {
    template: '<button><slot /><slot name="icon" /></button>',
    props: ['variant', 'type'],
  },
}

describe('CourseDetailsModal', () => {
  const baseCurso = {
    id: '1',
    titulo: 'Curso Teste',
    carga_horaria: 40,
    ano_gd: '2025',
  }

  it('shows certificate button for Realizado status', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Realizado',
          certificado_file_path: '/uploads/cert.pdf',
        },
      },
    })

    await nextTick()

    // Check computed values via the rendered HTML
    const html = wrapper.html()
    expect(html).toContain('Visualizar Certificado')
  })

  it('shows certificate button for Concluído status', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Concluído',
          certificado_link: 'https://example.com/cert',
        },
      },
    })

    await nextTick()

    expect(wrapper.html()).toContain('Ver Certificado Online')
  })

  it('shows certificate button for Validado status', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Validado',
          certificado_file_path: '/uploads/cert.pdf',
        },
      },
    })

    await nextTick()

    expect(wrapper.html()).toContain('Visualizar Certificado')
  })

  it('hides certificate button for Pendente status', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Pendente',
          certificado_file_path: '/uploads/cert.pdf',
        },
      },
    })

    await nextTick()

    expect(wrapper.html()).not.toContain('Visualizar Certificado')
  })

  it('hides certificate button when no certificate', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Realizado',
        },
      },
    })

    await nextTick()

    expect(wrapper.html()).not.toContain('Visualizar Certificado')
  })

  it('shows send certificate button for Em Andamento status', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Em Andamento',
          atribuicaoId: 'attr-1',
        },
      },
    })

    await nextTick()

    expect(wrapper.html()).toContain('Enviar Certificado')
  })

  it('displays correct status badge text for each status', async () => {
    for (const status of ['Pendente', 'Em Andamento', 'Realizado', 'Validado', 'Recusado']) {
      const wrapper = mount(CourseDetailsModal, {
        global: {
          stubs: ['teleport', 'transition'],
        },
        props: {
          show: true,
          curso: {
            ...baseCurso,
            status: status,
          },
        },
      })

      await nextTick()

      expect(wrapper.html()).toContain(status)
      wrapper.unmount()
    }
  })

  it('displays course details (titulo, carga_horaria, ano_gd)', async () => {
    const wrapper = mount(CourseDetailsModal, {
      global: {
        stubs: ['teleport', 'transition'],
      },
      props: {
        show: true,
        curso: {
          ...baseCurso,
          status: 'Pendente',
        },
      },
    })

    await nextTick()

    expect(wrapper.html()).toContain('Curso Teste')
    expect(wrapper.html()).toContain('40h')
    expect(wrapper.html()).toContain('2025')
  })
})
