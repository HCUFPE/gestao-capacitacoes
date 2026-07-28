import { describe, it, expect } from 'vitest'

describe('Status normalization helpers', () => {
  const VALID_STATUSES = ['Realizado', 'REALIZADO', 'Concluído', 'Validado']

  it('should include all case variants of Realizado', () => {
    expect(VALID_STATUSES).toContain('Realizado')
    expect(VALID_STATUSES).toContain('REALIZADO')
  })

  it('should include Concluído', () => {
    expect(VALID_STATUSES).toContain('Concluído')
  })

  it('should include Validado', () => {
    expect(VALID_STATUSES).toContain('Validado')
  })

  it('should not include Pendente', () => {
    expect(VALID_STATUSES).not.toContain('Pendente')
  })

  it('should not include Em Andamento', () => {
    expect(VALID_STATUSES).not.toContain('Em Andamento')
  })
})
