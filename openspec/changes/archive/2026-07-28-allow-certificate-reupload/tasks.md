## 1. Backend — Endpoint de Upload e Link (Upsert)

- [x] 1.1 Em `src/routers/certificado.py`, no endpoint `registrar_certificado_upload`, adicionar verificação do status da `atribuicao`. Se for `Validado` ou `Concluído`, lançar `HTTPException` 400.
- [x] 1.2 Em `src/routers/certificado.py`, no endpoint `registrar_certificado_upload`, verificar se a atribuição já possui um `certificado_id`. Se sim, obter o certificado existente do banco.
- [x] 1.3 Se um certificado existente possuir um `file_path`, removê-mo do disco (`os.remove`) após salvar o novo arquivo.
- [x] 1.4 Atualizar a entrada de `Certificado` existente (se houver) em vez de criar uma nova.
- [x] 1.5 Modificar o status da `Atribuicao` para `REALIZADO` usando o `atribuicao_controller` ao final do update.
- [x] 1.6 Repetir a mesma lógica de upsert (1.1, 1.2, 1.4, 1.5) no endpoint `registrar_certificado_link`. 

## 2. Testes Automatizados (Backend)

- [x] 2.1 Criar/atualizar testes em `tests/test_certificado_upload.py` para cobrir o cenário de re-upload de arquivo (garantir que o arquivo velho é deletado e que o status muda para REALIZADO).
- [x] 2.2 Criar/atualizar testes para o cenário de re-envio de link (garantir update do link e status REALIZADO).
- [x] 2.3 Criar teste verificando que a API rejeita re-upload se o status já for Validado/Concluído.

## 3. Frontend — Interface e Modal

- [x] 3.1 Em `CourseDetailsModal.vue`, renomear ou ajustar as condições que controlam a exibição do botão de envio de certificado para permitir que ele apareça também quando já existir um certificado, desde que o status seja `Realizado`, `Em Andamento` ou `Recusado`.
- [x] 3.2 Se um certificado já existir, o texto do botão de envio deve ser "Reenviar Certificado" ou similar.
- [x] 3.3 Garantir que o formulário de envio (ou `emit` correspondente) consiga lidar perfeitamente com a sobrescrita, recarregando os dados do curso após o upload bem-sucedido.

## 4. Testes Automatizados (Frontend)

- [x] 4.1 Adicionar teste no Vitest para `CourseDetailsModal.vue` garantindo que o botão de "Reenviar" aparece quando a atribuição tem status "Recusado" e um certificado anexado.
- [x] 4.2 Executar a suíte completa (pytest e vitest) para certificar-se de que nada quebrou.
