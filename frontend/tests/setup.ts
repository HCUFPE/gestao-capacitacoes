import { vi } from 'vitest'

// Mock Vue Toastification
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
    warning: vi.fn(),
  }),
}))

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    create: vi.fn(() => ({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    })),
  },
}))

// Mock window.open
Object.defineProperty(window, 'open', { value: vi.fn(), writable: true })

// Stub Vite env
vi.stubGlobal('import', { meta: { env: { VITE_API_BASE_URL: 'http://localhost:8000' } } })
