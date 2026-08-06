## 1. Backend Stats Endpoint Update

- [x] 1.1 Atualizar `src/controllers/dashboard_controller.py` para receber `user_id` opcional e retornar estatísticas pessoais e globais.
- [x] 1.2 Atualizar o schema `DashboardStatsResponse` em `src/schemas/dashboard.py` (ou `src/schemas/utils.py`) e a rota `/api/utils/stats` em `src/routers/utils.py`.
- [x] 1.3 Criar teste automatizado Pytest em `tests/test_dashboard_stats.py` validando os dados retornados.

## 2. Frontend Home Redesign & Polling

- [x] 2.1 Atualizar `frontend/src/views/Home.vue` para exibir dois conjuntos de cards ("Seu Panorama Pessoal" e "Visão Geral do Sistema").
- [x] 2.2 Implementar polling de 30s com detecção de visibilidade (`visibilitychange`) em `frontend/src/views/Home.vue`.
- [x] 2.3 Escrever teste Vitest para `Home.vue` garantindo renderização dos dois blocos de estatísticas.
