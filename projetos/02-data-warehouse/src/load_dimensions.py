from sqlalchemy import text
from src.database import engine
from src.extract import extrair_clientes
from src.transform import transformar_clientes
import pandas as pd

# Carrega os clientes no Data Warehouse
def carregar_dim_clientes(clientes):

    with engine.begin() as conexao:

        for _, cliente in clientes.iterrows():

            conexao.execute(
                text("""
                    INSERT INTO dw_vendas.dim_clientes
                    (cliente_id, nome, cidade, estado, data_cadastro)
                    VALUES (
                        :cliente_id,
                        :nome,
                        :cidade,
                        :estado,
                        :data_cadastro
                    )
                    ON CONFLICT (cliente_id) DO NOTHING
                """),
                {
                    "cliente_id": int(cliente["cliente_id"]),
                    "nome": cliente["nome"],
                    "cidade": cliente["cidade"],
                    "estado": cliente["estado"],
                    "data_cadastro": cliente["data_cadastro"]
                }
            )

    print(f"Clientes carregados: {len(clientes)}")
# Carrega os produtos no Data Warehouse
def carregar_dim_produtos(produtos):

    with engine.begin() as conexao:

        for _, produto in produtos.iterrows():

            conexao.execute(
                text("""
                    INSERT INTO dw_vendas.dim_produtos
                    (
                        produto_id,
                        nome_produto,
                        categoria,
                        preco_unitario,
                        custo_unitario
                    )
                    VALUES (
                        :produto_id,
                        :nome_produto,
                        :categoria,
                        :preco_unitario,
                        :custo_unitario
                    )
                    ON CONFLICT (produto_id) DO NOTHING
                """),
                {
                    "produto_id": int(produto["produto_id"]),
                    "nome_produto": produto["nome_produto"],
                    "categoria": produto["categoria"],
                    "preco_unitario": produto["preco_unitario"],
                    "custo_unitario": produto["custo_unitario"]
                }
            )

    print(f"Produtos carregados: {len(produtos)}")
    # Carrega as datas na dimensão de tempo
def carregar_dim_tempo(clientes, vendas):

    # Reúne as datas de cadastro e de venda
    datas_clientes = clientes["data_cadastro"]
    datas_vendas = vendas["data_venda"]

    # Combina todas as datas
    datas = pd.concat(
        [datas_clientes, datas_vendas]
    ).drop_duplicates().sort_values()

    with engine.begin() as conexao:

        for data in datas:

            conexao.execute(
                text("""
                    INSERT INTO dw_vendas.dim_tempo
                    (
                        data,
                        dia,
                        mes,
                        trimestre,
                        ano,
                        dia_semana
                    )
                    VALUES (
                        :data,
                        :dia,
                        :mes,
                        :trimestre,
                        :ano,
                        :dia_semana
                    )
                    ON CONFLICT (data) DO NOTHING
                """),
                {
                    "data": data.date(),
                    "dia": data.day,
                    "mes": data.month,
                    "trimestre": data.quarter,
                    "ano": data.year,
                    "dia_semana": data.isoweekday()
                }
            )

    print(f"Datas carregadas: {len(datas)}")