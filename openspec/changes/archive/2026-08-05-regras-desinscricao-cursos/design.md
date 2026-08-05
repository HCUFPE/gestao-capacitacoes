## Context

Atualmente o botão de desinscrição no frontend (`MeusCursos.vue`) aceita o status de inscrições concluídas/com certificado enviado, enquanto oculta o botão para inscrições "Em Andamento". O objetivo é inverter essa lógica para permitir o desvinculamento apenas quando o curso estiver "Em Andamento" (sem certificado).

## Goals / Non-Goals

**Goals:**
- Ajustar a condicional no Vue.js (`MeusCursos.vue`) para que o botão de desinscrição seja renderizado apenas quando `inscricao.status === 'Em Andamento'`.
- Implementar verificação no controlador de inscrição no backend (`inscricao_controller.py`) para rejeitar requisições de desinscrição em atribuições que possuam certificados.
- Adicionar testes de unidade no Frontend (Vitest) e Backend (Pytest).

**Non-Goals:**
- Alterar o fluxo de envio de certificados.
- Alterar telas de relatórios da UDP ou Chefia.

## Decisions

- **Inversão da condicional Vue**: Substituir `['Realizado', 'Concluído', 'Validado'].includes(inscricao.status)` por `inscricao.status === 'Em Andamento'`.
- **Validação no backend**: No método `remover_inscricao`, verificar se a atribuição possui `certificado_id` diferente de `None` ou status diferente de `Em Andamento`. Lançar `HTTPException(400)` se houver bloqueio.

## Risks / Trade-offs

- [Risco]: Usuário tentando desinscrever-se via chamada direta à API (ex: via devtools ou script).
  - *Mitigação*: Validação estrita no backend lançando exceção HTTP 400.
