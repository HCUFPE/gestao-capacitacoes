## 1. Fix certificate view/download in CourseDetailsModal

- [x] 1.1 Verificar e corrigir `openDetailsModal` em MeusCursos.vue para garantir que `certificado_id`, `certificado_file_path` e `certificado_link` sejam passados corretamente ao CourseDetailsModal tanto para inscrições quanto para atribuições
- [x] 1.2 Validar que `showCertificateButton` no CourseDetailsModal.vue funciona para todos os status com certificado (Realizado, Concluído, Validado) — remover status redundante 'REALIZADO' se já normalizado
- [x] 1.3 Testar fluxo completo: abrir modal → clicar em "Baixar Certificado" → arquivo abre/baixa corretamente
- [x] 1.4 Testar tratamento de erro: arquivo inexistente → mensagem "Certificado não disponível"

## 2. Add certificate replacement (re-upload) capability

- [x] 2.1 Adicionar botão "Reenviar certificado" no CourseDetailsModal.vue quando status for Realizado/Validado/Concluído (certificado já existe)
- [x] 2.2 Adicionar botão "Reenviar certificado" nos CourseCard de MeusCursos.vue para cursos com certificado enviado
- [x] 2.3 Validar backend: confirmar que POST /api/certificados/upload cria novo Certificado e atualiza Atribuicao.certificado_id corretamente (comportamento já existente)
- [x] 2.4 Validar que a Inscricao do usuário é preservada após re-upload do certificado
- [x] 2.5 Adicionar mensagem de sucesso diferenciada: "Certificado substituído com sucesso!" vs "Certificado enviado com sucesso!" no CertificateUploadModal

## 3. Fix PDF export layout (no truncation)

- [x] 3.1 Calcular larguras de coluna proporcionais no pdf_helper.py baseadas na largura da página letter (816pts) menos margens
- [x] 3.2 Adicionar `colWidths` na criação da Table do reportlab
- [x] 3.3 Habilitar word wrap automático para células de texto longo (nome_profissional, nome_curso)
- [x] 3.4 Ajustar margens e padding da tabela para evitar cortes laterais
- [x] 3.5 Adicionar quebra de página automática se o conteúdo exceder a página
- [x] 3.6 Validar visualmente o PDF gerado com dados de teste contendo nomes e cursos longos

## 4. Testing and validation

- [x] 4.1 Testar upload de certificado → visualização no modal → download do arquivo
- [x] 4.2 Testar substituição de certificado → apenas novo certificado aparece como ativo
- [x] 4.3 Testar que inscrição é preservada após substituição
- [x] 4.4 Testar exportação PDF com dados longos → nenhum campo cortado
- [x] 4.5 Testar exportação Excel → todos os campos presentes
