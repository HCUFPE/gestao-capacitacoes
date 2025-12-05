SELECT
    rap.usuario AS id,
    pf.nome AS nome,
    rap.email AS email,
    LPAD(pf.cpf::text, 11, '0') AS cpf,
    CASE WHEN rap.vin_codigo = 1 THEN
        'RJU - UFPE'
    WHEN rap.vin_codigo = 2 THEN
        'NASS - UFPE'
    WHEN rap.vin_codigo = 3 THEN
        'RESIDENTE'
    WHEN rap.vin_codigo = 4 THEN
        'EBSERH - CLT'
    WHEN rap.vin_codigo = 5 THEN
        'TERCEIRIZADO'
    WHEN rap.vin_codigo = 6 THEN
        'EBSERH - REQUISITADO'
    WHEN rap.vin_codigo = 7 THEN
        'BOLSISTA - ESTAGIARIO'
    WHEN rap.vin_codigo = 8 THEN
        'PROFESSOR'
    WHEN rap.vin_codigo = 9 THEN
        'VOLUNTARIO'
    WHEN rap.vin_codigo = 10 THEN
        'ESTUDANTE'
    ELSE
        'DESCONHECIDO'
    END AS vinculo
FROM
    agh.rap_servidores rap
    LEFT JOIN agh.rap_pessoas_fisicas pf ON pf.codigo = rap.pes_codigo
WHERE
    rap.ind_situacao = 'A'
    AND rap.usuario IS NOT NULL;

