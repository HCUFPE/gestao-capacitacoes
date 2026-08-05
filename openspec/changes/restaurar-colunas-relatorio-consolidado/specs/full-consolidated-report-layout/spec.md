## ADDED Requirements

### Requirement: Exibição das 11 Colunas no Relatório Consolidado
A interface do `RelatorioConsolidado.vue` SHALL exibir as 11 colunas de dados completas com suporte a ícones e badges coloridas.

#### Scenario: Renderização completa das colunas
- **WHEN** o relatório consolidado for carregado na tela
- **THEN** a tabela DEVE apresentar exatamente as 11 colunas: Nome, Vínculo, Setor, Curso, Plataforma, CH, Ano GD, Status, Envio Certificado, Certificado Enviado e Certificado.

#### Scenario: Visualização de ícone e cores
- **WHEN** os dados forem exibidos
- **THEN** a coluna Status DEVE ser formatada em badge colorida e a coluna Certificado Enviado DEVE exibir um ícone representativo de sucesso ou pendência.
