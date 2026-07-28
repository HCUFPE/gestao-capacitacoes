## Context

O sistema de Gestão de Capacitações é uma aplicação full-stack (FastAPI + Vue 3) para gerenciar cursos de capacitação EAD em uma organização com hierarquia (Trabalhador → Chefia → UDP). A autenticação é integrada ao Active Directory corporativo, com dados do usuário sincronizados no banco local SQLite. Dados externos de pacientes/servidores são consumidos via PostgreSQL (AGHU).

O sistema já possui 8 módulos backend, 10 views frontend, 20+ migrations Alembic e um provider pattern funcional. Contudo, carece de especificações formais que documentem requisitos, contratos API e fluxos de negócio.

## Goals / Non-Goals

**Goals:**
- Documentar todas as 7 capabilities do sistema com specs formais (requisitos + cenários testáveis)
- Estabelecer contratos API claros para cada domínio (endpoints, perfis, payloads, respostas)
- Documentar a arquitetura de provedores (interface → implementações → estratégia) como padrão reutilizável
- Mapear modelos de dados, relações e constraints existentes
- Fornecer base para validação futura de mudanças via `openspec validate`

**Non-Goals:**
- Modificar qualquer código de aplicação
- Adicionar novas funcionalidades ou alterar comportamento existente
- Criar tests automáticos a partir dos cenários (isso seria uma mudança futura)
- Refatorar a estrutura do projeto

## Decisions

### 1. Uma spec por capability de domínio

Cada spec cobre um domínio funcional independente (auth, cursos, inscrições, etc.). Isso permite que mudanças futuras afetem apenas a spec relevante, sem impacto colateral. A decisão foi baseada na separação natural dos routers do FastAPI e na coesão dos controllers.

**Alternativa considerada**: Uma única spec monolítica — rejeitada por dificultar rastreamento de mudanças e evolução incremental.

### 2. Cenários baseados no comportamento real existente

Os cenários dos specs refletem o comportamento já implementado, não o desejado. Isso garante que o primeiro `openspec validate` passe — as specs documentam a realidade, não aspirações.

**Alternativa considerada**: Especificar o estado ideal (com melhorias) — rejeitada pois confundiria documentação com backlog.

### 3. Design.md central, specs modulares

O design.md cobre decisões arquiteturais cross-cutting (provider pattern, dual DB, auth), enquanto cada spec detalha requisitos de domínio. Isso evita duplicação e mantém cada artefato focado.

### 4. Nomenclatura em kebab-case para capabilities

Segue o padrão OpenSpec e a convenção de pastas/arquivos do projeto. Ex: `course-assignment`, `certificate-validation`.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Specs desatualizam rapidamente com mudanças no código | Usar o workflow OpenSpec: toda mudança futura passa por spec delta antes da implementação |
| Documentação muito detalhada torna difícil manutenção | Manter foco em comportamento observável (API contracts, fluxos) — não em detalhes internos |
| Specs muito genéricas não servem como teste | Cada requirement tem pelo menos um cenário WHEN/THEN concreto e testável |
