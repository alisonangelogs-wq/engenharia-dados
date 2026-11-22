from sqlalchemy import text
from src.database import engine


# Carrega as vendas na tabela fato do Data Warehouse
def carregar_fato_vendas(vendas):

    with engine.begin() as conexao:

        # Recupera os códigos internos dos clientes
        clientes = dict(
            conexao.execute(
                text("""
                    SELECT cliente_id, sk_cliente
                    FROM dw_vendas.dim_clientes
                """)
            ).all()
        )

        # Recupera os códigos internos dos produtos
        produtos = dict(
            conexao.execute(
                text("""
                    SELECT produto_id, sk_produto
                    FROM dw_vendas.dim_produtos
                """)
            ).all()
        )

        # Recupera os códigos internos das datas
        tempos = dict(
            conexao.execute(
                text("""
                    SELECT data, sk_tempo
                    FROM dw_vendas.dim_tempo
                """)
            ).all()
        )

        # Percorre cada venda extraída e transformada
        for _, venda in vendas.iterrows():

            cliente_id = int(venda["cliente_id"])
            produto_id = int(venda["produto_id"])
            data_venda = venda["data_venda"].date()

            # Verifica se as três dimensões possuem os registros
            if cliente_id not in clientes:
                raise ValueError(
                    f"Cliente não encontrado: {cliente_id}"
                )

            if produto_id not in produtos:
                raise ValueError(
                    f"Produto não encontrado: {produto_id}"
                )

            if data_venda not in tempos:
                raise ValueError(
                    f"Data não encontrada: {data_venda}"
                )

            # Insere a venda utilizando as chaves substitutas
            conexao.execute(
                text("""
                    INSERT INTO dw_vendas.fato_vendas
                    (
                        venda_id,
                        sk_cliente,
                        sk_produto,
                        sk_tempo,
                        quantidade,
                        valor_unitario,
                        valor_total
                    )
                    VALUES (
                        :venda_id,
                        :sk_cliente,
                        :sk_produto,
                        :sk_tempo,
                        :quantidade,
                        :valor_unitario,
                        :valor_total
                    )
                    ON CONFLICT (venda_id) DO NOTHING
                """),
                {
                    "venda_id": int(venda["venda_id"]),
                    "sk_cliente": clientes[cliente_id],
                    "sk_produto": produtos[produto_id],
                    "sk_tempo": tempos[data_venda],
                    "quantidade": int(venda["quantidade"]),
                    "valor_unitario": venda["valor_unitario"],
                    "valor_total": venda["valor_total"]
                }
            )

    print(f"Vendas processadas: {len(vendas)}")