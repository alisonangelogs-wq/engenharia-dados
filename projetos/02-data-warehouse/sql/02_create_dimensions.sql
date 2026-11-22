CREATE TABLE IF NOT EXISTS dw_vendas.dim_clientes (
    sk_cliente SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100),
    estado CHAR(2),
    data_cadastro DATE
);
-- Cria a dimensão de produtos
CREATE TABLE IF NOT EXISTS dw_vendas.dim_produtos (
    sk_produto SERIAL PRIMARY KEY,
    produto_id INTEGER NOT NULL UNIQUE,
    nome_produto VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    preco_unitario NUMERIC(12,2) NOT NULL,
    custo_unitario NUMERIC(12,2) NOT NULL
);
-- Cria a dimensão de tempo
CREATE TABLE IF NOT EXISTS dw_vendas.dim_tempo (
    sk_tempo SERIAL PRIMARY KEY,
    data DATE NOT NULL UNIQUE,
    dia INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL
);