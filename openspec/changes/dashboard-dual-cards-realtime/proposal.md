## Why

Para dar clareza completa aos usuários (servidores, chefias e UDP), a tela inicial (`Home.vue`) deve exibir tanto os indicadores pessoais do usuário (suas inscrições e certificados) quanto a visão geral do sistema. Além disso, as estatísticas devem ser atualizadas automaticamente de forma econômica, pausando quando a aba não estiver visível para economizar recursos do servidor.

## What Changes

- **Backend**: Atualizar `/api/utils/stats` para retornar tanto os dados globais da plataforma quanto os dados pessoais do usuário logado (`minhas_inscricoes`, `meus_certificados_enviados`, `meus_certificados_validados`).
- **Frontend (`Home.vue`)**:
  - Organizar os cards em dois blocos claros: **"Seu Panorama Pessoal"** e **"Visão Geral do Sistema"**.
  - Implementar atualização periódica (polling de 30s) integrada à Page Visibility API, que interrompe as chamadas quando a aba está em segundo plano e atualiza imediatamente ao retornar o foco.

## Capabilities

### New Capabilities
- `dashboard-dual-cards-realtime`: Exibição dividida de cards pessoais e globais com atualização em tempo real econômica por detecção de foco da janela.

### Modified Capabilities

## Impact

- **Backend**: `src/controllers/dashboard_controller.py`, `src/routers/utils.py`, `src/schemas/dashboard.py`.
- **Frontend**: `frontend/src/views/Home.vue`.
- **Testes**: Pytest e Vitest.
