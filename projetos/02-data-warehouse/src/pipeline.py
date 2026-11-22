from src.extract import extrair_dados
from src.transform import transformar_dados

from src.load_dimensions import (
    carregar_dim_clientes,
    carregar_dim_produtos,
    carregar_dim_tempo
)

from src.load_fact import carregar_fato_vendas


# Executa o processo completo de ETL
def executar_pipeline():

    print("\n=== INICIANDO DATA WAREHOUSE ===")

    # 1. Extração
    print("\nETAPA 1 - EXTRAÇÃO")

    dados = extrair_dados()

    # 2. Transformação
    print("\nETAPA 2 - TRANSFORMAÇÃO")

    clientes, produtos, vendas = transformar_dados(
        dados["clientes"],
        dados["produtos"],
        dados["vendas"]
    )

    # 3. Carga das dimensões
    print("\nETAPA 3 - CARGA DAS DIMENSÕES")

    carregar_dim_clientes(clientes)
    carregar_dim_produtos(produtos)
    carregar_dim_tempo(clientes, vendas)

    # 4. Carga da tabela fato
    print("\nETAPA 4 - CARGA DA TABELA FATO")

    carregar_fato_vendas(vendas)

    print("\n=== DATA WAREHOUSE CONCLUÍDO ===")


if __name__ == "__main__":
    executar_pipeline()