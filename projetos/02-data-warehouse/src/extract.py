import pandas as pd
from pathlib import Path
# Identifica o diretório principal deste projeto
DIRETORIO_PROJETO = Path(__file__).resolve().parent.parent
# Identifica a pasta que contém os arquivos CSV
DIRETORIO_DADOS = DIRETORIO_PROJETO / "dados"
# Define o caminho de cada arquivo CSV
ARQUIVO_CLIENTES = DIRETORIO_DADOS / "clientes.csv"
ARQUIVO_PRODUTOS = DIRETORIO_DADOS / "produtos.csv"
ARQUIVO_VENDAS = DIRETORIO_DADOS / "vendas.csv"
# Extrai os dados dos clientes
def extrair_clientes():
    clientes = pd.read_csv(ARQUIVO_CLIENTES)

    print(f"Clientes extraídos: {len(clientes)}")

    return clientes
# Extrai os dados dos produtos
def extrair_produtos():
    produtos = pd.read_csv(ARQUIVO_PRODUTOS)

    print(f"Produtos extraídos: {len(produtos)}")

    return produtos
# Extrai os dados das vendas
def extrair_vendas():
    vendas = pd.read_csv(ARQUIVO_VENDAS)

    print(f"Vendas extraídas: {len(vendas)}")

    return vendas
# Executa todas as extrações
def extrair_dados():
    clientes = extrair_clientes()
    produtos = extrair_produtos()
    vendas = extrair_vendas()

    return {
        "clientes": clientes,
        "produtos": produtos,
        "vendas": vendas
    }