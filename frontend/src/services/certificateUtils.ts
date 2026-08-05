/**
 * Utilitário compartilhado para construção de URLs de certificado.
 * Sempre usa a rota da API `/api/certificados/download/` para garantir
 * Content-Type correto e Content-Disposition inline.
 */

const BACKEND_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export interface CertificateItem {
  certificado_file_path?: string | null;
  certificado_link?: string | null;
}

/**
 * Retorna a URL para visualização de um certificado.
 * - Se há um `certificado_file_path`, usa a rota da API para download/visualização.
 * - Se há um `certificado_link`, retorna o link externo diretamente.
 * - Caso contrário, retorna null.
 */
export function getCertificateUrl(item: CertificateItem): string | null {
  if (item.certificado_link) {
    return item.certificado_link;
  }
  if (item.certificado_file_path) {
    const fileName = item.certificado_file_path.split(/[\/\\]/).pop();
    return `${BACKEND_BASE_URL}/api/certificados/download/${fileName}`;
  }
  return null;
}
