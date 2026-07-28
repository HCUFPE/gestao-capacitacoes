## ADDED Requirements

### Requirement: Visualização Inline de Certificado no Navegador
O sistema SHALL permitir a visualização direta (inline) de certificados nos formatos PDF e imagem (PNG, JPG, JPEG, GIF) no navegador do usuário, sem forçar o download automático do arquivo.

#### Scenario: Visualização direta de imagem de certificado
- **WHEN** o usuário ou gestor solicita a visualização de um certificado em formato de imagem (PNG, JPG, JPEG, GIF)
- **THEN** o sistema SHALL responder com o Content-Type correspondente à imagem (ex: `image/png`) e o cabeçalho `Content-Disposition: inline`, permitindo que o navegador renderize a imagem em uma nova aba.

#### Scenario: Visualização direta de certificado em PDF
- **WHEN** o usuário ou gestor solicita a visualização de um certificado em formato PDF
- **THEN** o sistema SHALL responder com o Content-Type `application/pdf` e o cabeçalho `Content-Disposition: inline`, permitindo que o navegador abra o PDF em uma nova aba.

### Requirement: URL Unificada de Certificado
Todos os componentes do frontend SHALL construir URLs de certificado exclusivamente via a rota da API `/api/certificados/download/`, nunca por acesso direto a caminhos estáticos como `/static/uploads/`.

#### Scenario: Link de certificado nos relatórios de chefia
- **WHEN** o gestor clica em "Visualizar" no certificado de um subordinado na tela de Progresso Individual
- **THEN** o sistema SHALL abrir o certificado usando a URL da API `/api/certificados/download/{fileName}` em uma nova aba.

#### Scenario: Link de certificado no relatório consolidado
- **WHEN** o gestor ou UDP clica em "Visualizar" no certificado de um colaborador na tela de Relatório Consolidado
- **THEN** o sistema SHALL abrir o certificado usando a URL da API `/api/certificados/download/{fileName}` em uma nova aba.

#### Scenario: Link de certificado no modal de detalhes de usuário
- **WHEN** o gestor ou UDP clica em "Visualizar" no modal de detalhes do usuário
- **THEN** o sistema SHALL abrir o certificado usando a URL da API `/api/certificados/download/{fileName}` em uma nova aba.

### Requirement: Texto de Botão Coerente com Visualização Inline
O texto do botão de visualização de certificado SHALL refletir o comportamento real (visualização inline), independentemente do formato do arquivo.

#### Scenario: Botão de certificado PDF
- **WHEN** o certificado associado é um arquivo PDF
- **THEN** o botão SHALL exibir "Visualizar Certificado" (não "Baixar Certificado"), pois o arquivo será aberto inline no navegador.
