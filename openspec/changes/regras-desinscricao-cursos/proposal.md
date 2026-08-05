## Why

Atualmente, o botão "Desinscrever-se" permanece visível mesmo após o envio do certificado do curso, permitindo que usuários excluam acidentalmente inscrições concluídas e percam seus comprovantes. Além disso, o botão não fica disponível durante a fase em que o curso está apenas "Em Andamento" (sem certificado enviado), impedindo a desistência legítima.

## What Changes

- Exibir o botão "Desinscrever-se" exclusivamente para inscrições/atribuições no status **"Em Andamento"** (sem certificado anexado).
- Ocultar o botão "Desinscrever-se" assim que o usuário realizar o envio do certificado (status `Realizado`, `Validado` ou `Concluído`).
- Adicionar validação de segurança no Backend (`DELETE /api/inscricoes/{id}`) para recusar desinscrições caso a atribuição possua um certificado anexado.

## Capabilities

### New Capabilities
- `course-unenrollment-rules`: Regras para controle de visibilidade do botão de desinscrição e validação backend anti-exclusão de inscrições com certificado.

### Modified Capabilities

## Impact

- Frontend: `frontend/src/views/MeusCursos.vue`
- Backend: `src/routers/inscricao.py`, `src/controllers/inscricao_controller.py`
- Testes: Testes unitários para componente Vue e controller FastAPI.
