## Context

Os usuários necessitam acompanhar simultaneamente o seu próprio desempenho (suas inscrições e envios de certificados) e o indicador global da instituição. A atualização deve ser em tempo real porém sem desperdício de infraestrutura.

## Goals / Non-Goals

**Goals:**
- Atualizar `/api/utils/stats` no backend para incluir os contadores pessoais do `user_id` logado (se fornecido/autenticado).
- Redesenhar `Home.vue` dividindo a estatística em dois blocos de cards ("Seu Panorama Pessoal" e "Visão Geral do Sistema").
- Implementar timer reativo com `document.addEventListener('visibilitychange', ...)` para pausar a busca em background.

**Non-Goals:**
- Implementar WebSockets complexos ou infraestrutura dedicada de realtime.

## Decisions

- **Decisão 1**: Atualizar a resposta de `get_dashboard_stats` para incluir:
  - `pessoal`: `{ minhas_inscricoes: int, meus_certificados_enviados: int, meus_certificados_validados: int }`
  - `global`: `{ total_cursos: int, total_inscricoes: int, total_certificados_validados: int, total_usuarios: int }`
- **Decisão 2**: Usar Polling de 30 segundos com controle de visibilidade da página no Vue (`onMounted` / `onUnmounted`).
