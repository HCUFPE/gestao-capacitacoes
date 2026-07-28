## 1. Backend Controller & Endpoint

- [ ] 1.1 Extrair lógica de importação de CSV do `import_users.py` para `src/controllers/usuario_controller.py` (ou módulo de serviço dedicado).
- [ ] 1.2 Criar endpoint `POST /admin/usuarios/importar-csv` em `src/routers/admin.py` recebendo `UploadFile` e protegido pela dependência `is_udp`.
- [ ] 1.3 Adicionar testes unitários/integração no Pytest em `tests/test_admin_csv_import.py` cobrindo cenários com sucesso, arquivo inválido e acesso não autorizado.

## 2. Frontend Integration

- [ ] 2.1 Adicionar método `importarUsuariosCsv` no serviço de API do frontend (`src/services/` ou `src/api/`).
- [ ] 2.2 Criar componente de modal de importação `ImportUsuariosModal.vue` com seletor de arquivo, indicador de progresso e exibição do resumo de resultados.
- [ ] 2.3 Integrar o componente `ImportUsuariosModal.vue` na tela de administração/usuários.
- [ ] 2.4 Criar testes de componente com Vitest para `ImportUsuariosModal.vue` cobrindo renderização, seleção de arquivo e exibição do retorno da API.
