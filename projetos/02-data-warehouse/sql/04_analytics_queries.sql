-- CONSULTA 1: FATURAMENTO TOTAL

SELECT
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS unidades_vendidas,
    SUM(valor_total) AS faturamento_total,
    AVG(valor_total) AS ticket_medio
FROM dw_vendas.fato_vendas;
-- CONSULTA 2: FATURAMENTO POR CATEGORIA

SELECT
    p.categoria,
    COUNT(f.venda_id) AS total_vendas,
    SUM(f.quantidade) AS unidades_vendidas,
    SUM(f.valor_total) AS faturamento
FROM dw_vendas.fato_vendas AS f

INNER JOIN dw_vendas.dim_produtos AS p
    ON f.sk_produto = p.sk_produto

GROUP BY p.categoria

ORDER BY faturamento DESC;
-- CONSULTA 3: FATURAMENTO POR CLIENTE

SELECT
    c.cliente_id,
    c.nome,
    c.cidade,
    COUNT(f.venda_id) AS total_compras,
    SUM(f.valor_total) AS faturamento_total
FROM dw_vendas.fato_vendas AS f

INNER JOIN dw_vendas.dim_clientes AS c
    ON f.sk_cliente = c.sk_cliente

GROUP BY
    c.cliente_id,
    c.nome,
    c.cidade

ORDER BY faturamento_total DESC;
-- CONSULTA 4: DESEMPENHO DE VENDAS POR PRODUTO

SELECT
    p.produto_id,
    p.nome_produto,
    p.categoria,
    COUNT(f.venda_id) AS total_vendas,
    SUM(f.quantidade) AS unidades_vendidas,
    SUM(f.valor_total) AS faturamento
FROM dw_vendas.fato_vendas AS f

INNER JOIN dw_vendas.dim_produtos AS p
    ON f.sk_produto = p.sk_produto

GROUP BY
    p.produto_id,
    p.nome_produto,
    p.categoria

ORDER BY faturamento DESC;
-- CONSULTA 5: FATURAMENTO POR MÊS

SELECT
    t.ano,
    t.mes,
    COUNT(f.venda_id) AS total_vendas,
    SUM(f.quantidade) AS unidades_vendidas,
    SUM(f.valor_total) AS faturamento
FROM dw_vendas.fato_vendas AS f

INNER JOIN dw_vendas.dim_tempo AS t
    ON f.sk_tempo = t.sk_tempo

GROUP BY
    t.ano,
    t.mes

ORDER BY
    t.ano,
    t.mes;
    -- CONSULTA 6: FATURAMENTO POR CIDADE

SELECT
    c.cidade,
    c.estado,
    COUNT(f.venda_id) AS total_vendas,
    SUM(f.quantidade) AS unidades_vendidas,
    SUM(f.valor_total) AS faturamento
FROM dw_vendas.fato_vendas AS f

INNER JOIN dw_vendas.dim_clientes AS c
    ON f.sk_cliente = c.sk_cliente

GROUP BY
    c.cidade,
    c.estado

ORDER BY
    faturamento DESC;