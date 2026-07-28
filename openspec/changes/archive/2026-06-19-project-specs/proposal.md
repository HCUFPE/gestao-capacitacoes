## Why

O sistema de Gestão de Capacitações está funcional, mas carece de documentação formal de especificações. Sem specs estruturadas, é difícil garantir consistência em mudanças futuras, onboardar novos desenvolvedores, e rastrear requisitos de negócio. Esta mudança estabelece a base spec-driven para todo o projeto.

## What Changes

- Criação de 7 especificações de capability cobrindo todos os domínios do sistema
- Documentação formal dos modelos de dados, fluxos de negócio e regras de acesso
- Definição clara dos contratos API existentes (endpoint, perfis necessários, payloads)
- Especificação da arquitetura de provedores (provider pattern) e dual database
- Criação de um design.md central mapeando a arquitetura completa do sistema

## Capabilities

### New Capabilities

- `authentication`: Autenticação via Active Directory, JWT access tokens, refresh tokens (HttpOnly cookie), sincronização de usuário no BD local, perfis e guardas de acesso
- `user-management`: Gestão de usuários com 3 perfis (Trabalhador, Chefia, UDP), sincronização AD, atualização de perfil por UDP
- `course-management`: CRUD de cursos EAD com metadados (tema, certificadora, carga horária, lotação), recomendação por lotação, cursos genéricos
- `enrollment`: Inscrição voluntária do usuário em cursos, com criação automática de atribuição vinculada, desinscrição, listagem de inscrições
- `course-assignment`: Atribuição obrigatória de cursos por Chefia/UDP, máquina de estados (Pendente → Em Andamento → Realizado → Concluído), tracking de conclusão
- `certificate-validation`: Upload de comprovante de conclusão (arquivo PDF ou link externo), validação/rejeição por Chefia/UDP, download de certificados
- `reporting`: Relatórios de conformidade por lotação, progresso individual, cursos populares, certificados pendentes, exportação Excel/PDF, dashboard com stats gerais

### Modified Capabilities

(nenhuma — são todas capabilities novas)

## Impact

- **Código-fonte**: Nenhum arquivo de aplicação será modificado — esta mudança é puramente documental
- **Estrutura do projeto**: Criação de `openspec/specs/<capability>/spec.md` para cada uma das 7 capabilities
- **Arquivos OpenSpec**: `proposal.md`, `design.md`, `tasks.md` em `openspec/changes/project-specs/`
- **Dependências**: Nenhuma nova dependência de runtime
- **API**: Sem alterações na API — apenas documentação dos contratos existentes
