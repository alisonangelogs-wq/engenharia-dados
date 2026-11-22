-- Cria a tabela fato de vendas
CREATE TABLE IF NOT EXISTS dw_vendas.fato_vendas (
    sk_venda BIGSERIAL PRIMARY KEY,
    venda_id INTEGER NOT NULL UNIQUE,

    sk_cliente INTEGER NOT NULL,
    sk_produto INTEGER NOT NULL,
    sk_tempo INTEGER NOT NULL,

    quantidade INTEGER NOT NULL,
    valor_unitario NUMERIC(12,2) NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL,

    CONSTRAINT fk_venda_cliente
        FOREIGN KEY (sk_cliente)
        REFERENCES dw_vendas.dim_clientes (sk_cliente),

    CONSTRAINT fk_venda_produto
        FOREIGN KEY (sk_produto)
        REFERENCES dw_vendas.dim_produtos (sk_produto),

    CONSTRAINT fk_venda_tempo
        FOREIGN KEY (sk_tempo)
        REFERENCES dw_vendas.dim_tempo (sk_tempo)
);