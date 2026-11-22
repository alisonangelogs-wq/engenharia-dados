
import pandas as pd
from unittest.mock import patch

from src.pipeline import executar_pipeline


def test_executar_pipeline():

    # Dados simulados da extração
    clientes = pd.DataFrame({
        "cliente_id": [1],
        "nome": ["Carlos"]
    })

    produtos = pd.DataFrame({
        "produto_id": [101],
        "nome_produto": ["Notebook"]
    })

    vendas = pd.DataFrame({
        "venda_id": [1001],
        "cliente_id": [1],
        "produto_id": [101]
    })

    dados_extraidos = {
        "clientes": clientes,
        "produtos": produtos,
        "vendas": vendas
    }

    # Simula as funções externas do pipeline
    with patch("src.pipeline.extrair_dados") as extrair, \
         patch("src.pipeline.transformar_dados") as transformar, \
         patch("src.pipeline.carregar_dim_clientes") as carga_clientes, \
         patch("src.pipeline.carregar_dim_produtos") as carga_produtos, \
         patch("src.pipeline.carregar_dim_tempo") as carga_tempo, \
         patch("src.pipeline.carregar_fato_vendas") as carga_fato:

        # Configura os retornos das simulações
        extrair.return_value = dados_extraidos

        transformar.return_value = (
            clientes,
            produtos,
            vendas
        )

        # Executa o pipeline
        executar_pipeline()

        # Verifica a extração
        extrair.assert_called_once()

        # Verifica a transformação
        transformar.assert_called_once_with(
            clientes,
            produtos,
            vendas
        )

        # Verifica a carga das dimensões
        carga_clientes.assert_called_once_with(clientes)
        carga_produtos.assert_called_once_with(produtos)
        carga_tempo.assert_called_once_with(clientes, vendas)

        # Verifica a carga da tabela fato
        carga_fato.assert_called_once_with(vendas)
