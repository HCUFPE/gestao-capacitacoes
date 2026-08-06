## ADDED Requirements

### Requirement: Exibição dupla de cards (Pessoal e Global) na Tela Inicial
A tela inicial (`Home.vue`) DEVE exibir dois conjuntos distintos de cards de estatísticas: um conjunto com os dados pessoais do usuário logado e outro com os dados globais do sistema.

#### Scenario: Visualização dos cards pessoais e globais
- **WHEN** qualquer usuário autenticado acessa a tela inicial
- **THEN** o sistema DEVE exibir a seção "Seu Panorama Pessoal" (inscrições, certificados enviados e certificados validados do usuário) e a seção "Visão Geral do Sistema" (total de cursos, inscrições globais, certificados validados globais e usuários).

### Requirement: Atualização econômica em tempo real (Polling Reativo)
A tela inicial DEVE atualizar periodicamente os contadores dos cards sem sobrecarregar o servidor.

#### Scenario: Pausa por inatividade de aba
- **WHEN** a aba do navegador perde o foco ou é minimizada (`document.hidden == true`)
- **THEN** o timer de atualização DEVE ser suspenso, não realizando nenhuma chamada ao servidor.

#### Scenario: Atualização ao focar a aba
- **WHEN** o usuário retorna o foco para a aba da aplicação (`visibilitychange` / `focus`)
- **THEN** os cards DEVEM realizar uma requisição imediata e retomar a atualização periódica.
