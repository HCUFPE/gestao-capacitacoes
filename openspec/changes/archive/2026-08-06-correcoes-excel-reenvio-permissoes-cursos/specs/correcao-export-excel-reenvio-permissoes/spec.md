## ADDED Requirements

### Requirement: Exportar Relatório Consolidado para Excel sem erro
O sistema DEVE permitir a geração e download do arquivo Excel (.xlsx) no Relatório Consolidado (tanto Chefia quanto UDP) sem erros HTTP 500.

#### Scenario: Download de relatório em Excel com sucesso
- **WHEN** o usuário clica no botão "Exportar Excel" na tela de Relatório Consolidado
- **THEN** o backend DEVE processar a requisição e retornar o arquivo `.xlsx` com o status HTTP 200

### Requirement: Reenvio de Certificados nos status Realizado e Recusado
O sistema DEVE exibir a opção "Reenviar Certificado" para o usuário caso a atribuição do curso esteja com status "Realizado" ou "Recusado".

#### Scenario: Reenviar certificado para curso realizado
- **WHEN** o usuário acessa a tela Meus Cursos ou Modal de Detalhes de um curso com status "Realizado" ou "Recusado"
- **THEN** o sistema DEVE exibir a opção "Reenviar" permitindo o envio de um novo arquivo de certificado

### Requirement: Restrição de Edição e Exclusão de Cursos a Chefia ou UDP
O sistema DEVE permitir o cadastro, alteração e deleção de cursos exclusivamente para usuários com perfis de Chefia ou UDP.

#### Scenario: Acesso permitido a Chefia e UDP
- **WHEN** um usuário com perfil "Chefia" ou "UDP" realiza a criação, edição ou exclusão de um curso
- **THEN** o sistema DEVE autorizar e processar a operação

#### Scenario: Acesso negado a outros perfis
- **WHEN** um usuário sem perfil "Chefia" ou "UDP" tenta realizar operações de alteração em cursos
- **THEN** o sistema DEVE negar o acesso retornando HTTP 403 ou bloqueando a rota no frontend
