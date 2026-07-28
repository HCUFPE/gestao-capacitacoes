## Context

O sistema possui três falhas no fluxo de certificados e exportação:

1. **Visualização de certificado**: O endpoint `/api/certificados/download/{file_name}` existe em `src/main.py` e funciona, mas o botão no CourseDetailsModal só aparece para statuses `['Realizado', 'REALIZADO', 'Concluído', 'Validado']` — o tratamento é inconsistente. O modal já faz HEAD check, porém a lógica pode falhar se o `certificado_file_path` ou `certificado_link` não forem passados corretamente do backend.

2. **Substituição de certificado**: Atualmente, o upload de certificado (`POST /api/certificados/upload`) sempre cria um novo registro Certificado e atualiza a Atribuicao. Porém, não há controle de qual certificado é "ativo" — múltiplos certificados podem ser criados para o mesmo user+curso, e a UI não oferece um botão explícito de "reenviar". O CertificateUploadModal funciona apenas para upload inicial, sem distinguir reenvio.

3. **PDF cortado**: O `pdf_helper.py` usa `reportlab` com `Table` simples sem larguras de coluna definidas, sem quebra de página inteligente e sem tratamento de texto longo. Colunas como `nome_profissional`, `nome_curso` e `cpf` podem exceder a largura da página letter (816pts).

## Goals / Non-Goals

**Goals:**
- Garantir visualização/download de certificado funcional em Meus Cursos e CourseDetailsModal
- Permitir reenvio/substituição de certificado sem perder a inscrição
- Apenas o certificado mais recente por user+curso é considerado ativo
- PDF exportado sem cortes de conteúdo, com layout responsivo

**Non-Goals:**
- Nova tela de validação de certificados (item 11 do brief)
- Atribuição granular de cursos (change separada)
- Filtros por ano/vínculo nos relatórios (change separada)
- Relatório consolidado Mentor (change separada)
- Visualização de certificados nos relatórios de chefia (change separada)

## Decisions

**Decision 1: Reusar endpoint de upload para substituição**
- O endpoint `POST /api/certificados/upload` já cria novo Certificado e atualiza a Atribuicao. Não é necessária nova rota.
- A diferenciação será feita no frontend (botão "Reenviar" vs "Enviar") e na mensagem exibida.
- Alternativa considerada: endpoint separado `PUT /api/certificados/substituir` — rejeitada por simplicidade, pois o comportamento backend é idêntico.

**Decision 2: Marcando certificado ativo via query, não via campo extra**
- Em vez de adicionar campo `is_active` ao modelo Certificado, a consulta sempre pega o certificado mais recente por `data_conclusao` (já existente na Atribuicao) ou pelo `certificado_id` apontado na Atribuicao.
- Como a Atribuicao já armazena `certificado_id` (FK), apenas o último update define qual é o ativo.
- Isso evita migration adicional.

**Decision 3: PDF com colunas automáticas e quebra de texto**
- Usar `reportlab.platypus.Table` com `colWidths` calculadas com base na largura da página.
- Adicionar `WordWrap` nos textos e `VALIGN` para alinhamento.
- Dividir o relatório em seções com quebra de página se necessário.
- Alternativa considerada: migrar para WeasyPrint ou pdfkit — rejeitada por adicionar dependência externa significativa.

**Decision 4: Botão "Reenviar certificado" no CourseDetailsModal e nos cards**
- Adicionar botão condicional no CourseDetailsModal quando status for Realizado/Validado/Concluído (certificado já enviado).
- Adicionar botão também nos CourseCard de MeusCursos quando certificado existe.
- O CertificateUploadModal será reutilizado sem alterações no backend.

## Risks / Trade-offs

[Certificados antigos permanecem no banco] → Não há cleanup automático. Mitigation: adicionar campo `substituido_em` no futuro se necessário. Para agora, o certificado_id da Atribuicao aponta sempre para o mais recente.

[PDF pode ser lento para muitos registros] → reportlab processa tudo em memória. Mitigation: para volumes atuais é aceitável. Se crescer, considerar paginação ou lazy loading.

[Upload sem autenticação no download] → O endpoint de download em `main.py` não requer autenticação. Mitigation: fora do escopo desta change — o arquivo já tem nome UUID, dificultando adivinhação.
