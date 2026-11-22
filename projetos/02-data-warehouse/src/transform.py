import pandas as pd


# Valida os dados dos clientes
def transformar_clientes(clientes):

    valores_ausentes = clientes.isnull().sum().sum()
    ids_duplicados = clientes["cliente_id"].duplicated().sum()

    if valores_ausentes > 0:
        raise ValueError(
            f"Existem {valores_ausentes} valores ausentes nos clientes."
        )

    if ids_duplicados > 0:
        raise ValueError(
            f"Existem {ids_duplicados} IDs duplicados nos clientes."
        )

    print("Validação dos clientes concluída sem problemas.")

    return clientes


# Valida os dados dos produtos
def transformar_produtos(produtos):

    valores_ausentes = produtos.isnull().sum().sum()
    ids_duplicados = produtos["produto_id"].duplicated().sum()
    precos_invalidos = (produtos["preco_unitario"] <= 0).sum()
    custos_invalidos = (produtos["custo_unitario"] <= 0).sum()

    if valores_ausentes > 0:
        raise ValueError(
            f"Existem {valores_ausentes} valores ausentes nos produtos."
        )

    if ids_duplicados > 0:
        raise ValueError(
            f"Existem {ids_duplicados} IDs duplicados nos produtos."
        )

    if precos_invalidos > 0:
        raise ValueError(
            f"Existem {precos_invalidos} preços inválidos nos produtos."
        )

    if custos_invalidos > 0:
        raise ValueError(
            f"Existem {custos_invalidos} custos inválidos nos produtos."
        )

    print("Validação dos produtos concluída sem problemas.")

    return produtos

# Valida os dados das vendas
def transformar_vendas(vendas):

    valores_ausentes = vendas.isnull().sum().sum()
    ids_duplicados = vendas["venda_id"].duplicated().sum()
    quantidades_invalidas = (vendas["quantidade"] <= 0).sum()
    valores_invalidos = (vendas["valor_unitario"] <= 0).sum()

    if valores_ausentes > 0:
        raise ValueError(
            f"Existem {valores_ausentes} valores ausentes nas vendas."
        )

    if ids_duplicados > 0:
        raise ValueError(
            f"Existem {ids_duplicados} IDs duplicados nas vendas."
        )

    if quantidades_invalidas > 0:
        raise ValueError(
            f"Existem {quantidades_invalidas} quantidades inválidas nas vendas."
        )

    if valores_invalidos > 0:
        raise ValueError(
            f"Existem {valores_invalidos} valores unitários inválidos nas vendas."
        )

    print("Validação das vendas concluída sem problemas.")

    return vendas

# Valida os relacionamentos entre vendas, clientes e produtos
def validar_relacionamentos(clientes, produtos, vendas):

    clientes_invalidos = vendas[
        ~vendas["cliente_id"].isin(clientes["cliente_id"])
    ]

    produtos_invalidos = vendas[
        ~vendas["produto_id"].isin(produtos["produto_id"])
    ]

    if not clientes_invalidos.empty:
        raise ValueError(
            f"Existem {len(clientes_invalidos)} vendas com clientes inexistentes."
        )

    if not produtos_invalidos.empty:
        raise ValueError(
            f"Existem {len(produtos_invalidos)} vendas com produtos inexistentes."
        )

    print("Relacionamentos entre vendas, clientes e produtos válidos.")

    return clientes_invalidos, produtos_invalidos


# Converte as colunas de datas
def transformar_datas(clientes, vendas):

    clientes["data_cadastro"] = pd.to_datetime(
        clientes["data_cadastro"], errors="raise"
    )

    vendas["data_venda"] = pd.to_datetime(
        vendas["data_venda"], errors="raise"
    )

    print("Tipo da data de cadastro:", clientes["data_cadastro"].dtype)
    print("Tipo da data de venda:", vendas["data_venda"].dtype)

    return clientes, vendas


# Calcula o valor total de cada venda
def calcular_total_vendas(vendas):

    vendas["valor_total"] = (
        vendas["quantidade"] * vendas["valor_unitario"]
    )

    print("Valor total das vendas calculado.")
    print("Faturamento total:", vendas["valor_total"].sum())

    return vendas

# Executa todas as transformações
def transformar_dados(clientes, produtos, vendas):

    # 1. Valida os dados dos clientes
    clientes = transformar_clientes(clientes)

    # 2. Valida os dados dos produtos
    produtos = transformar_produtos(produtos)

    # 3. Valida os dados das vendas
    vendas = transformar_vendas(vendas)

    # 4. Valida os relacionamentos
    validar_relacionamentos(clientes, produtos, vendas)

    # 5. Converte as datas
    clientes, vendas = transformar_datas(clientes, vendas)

    # 6. Calcula o valor total das vendas
    vendas = calcular_total_vendas(vendas)

    # 7. Retorna os três conjuntos de dados
    return clientes, produtos, vendas
