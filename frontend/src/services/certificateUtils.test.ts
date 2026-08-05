import { describe, it, expect, vi } from 'vitest';
import { getCertificateUrl } from './certificateUtils';

// Mock import.meta.env
vi.stubEnv('VITE_API_BASE_URL', 'http://localhost:8000');

describe('getCertificateUrl', () => {
  it('returns null when neither file_path nor link is present', () => {
    expect(getCertificateUrl({})).toBeNull();
    expect(getCertificateUrl({ certificado_file_path: null, certificado_link: null })).toBeNull();
  });

  it('returns the external link when certificado_link is present', () => {
    const item = { certificado_link: 'https://example.com/cert.pdf' };
    expect(getCertificateUrl(item)).toBe('https://example.com/cert.pdf');
  });

  it('returns API URL when certificado_file_path is present', () => {
    const item = { certificado_file_path: 'src/static/uploads/abc-123.pdf' };
    const result = getCertificateUrl(item);
    expect(result).toBe('/api/certificados/download/abc-123.pdf');
  });

  it('extracts only the filename from a full path', () => {
    const item = { certificado_file_path: '/some/deep/path/to/uuid-file.png' };
    const result = getCertificateUrl(item);
    expect(result).toContain('/api/certificados/download/uuid-file.png');
    expect(result).not.toContain('/some/deep/path');
  });

  it('extracts only the filename from a Windows full path', () => {
    const item = { certificado_file_path: 'C:\\some\\deep\\path\\to\\uuid-file.pdf' };
    const result = getCertificateUrl(item);
    expect(result).toContain('/api/certificados/download/uuid-file.pdf');
    expect(result).not.toContain('C:\\some\\deep\\path');
  });

  it('prioritizes certificado_link over certificado_file_path', () => {
    const item = {
      certificado_link: 'https://external.com/cert',
      certificado_file_path: 'src/static/uploads/local-file.pdf',
    };
    expect(getCertificateUrl(item)).toBe('https://external.com/cert');
  });

  it('handles image file extensions correctly in the URL', () => {
    const item = { certificado_file_path: 'uploads/photo.jpg' };
    const result = getCertificateUrl(item);
    expect(result).toBe('/api/certificados/download/photo.jpg');
  });
});
