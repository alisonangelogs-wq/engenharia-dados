
import pandas as pd
import pytest

from src.transform import (
    transformar_clientes,
    transformar_produtos,
    transformar_vendas,
    validar_relacionamentos,
    transformar_datas,
    calcular_total_vendas
)


# TESTES DE CLIENTES

def test_transformar_clientes():
    clientes = pd.DataFrame({
        "cliente_id": [1, 2],
        "nome": ["Carlos", "Maria"]
    })

    resultado = transformar_clientes(clientes)

    assert len(resultado) == 2
    assert resultado["cliente_id"].is_unique


def test_clientes_com_valores_ausentes():
    clientes = pd.DataFrame({
        "cliente_id": [1, 2],
        "nome": ["Carlos", None]
    })

    with pytest.raises(ValueError, match="valores ausentes"):
        transformar_clientes(clientes)


def test_clientes_com_ids_duplicados():
    clientes = pd.DataFrame({
        "cliente_id": [1, 1],
        "nome": ["Carlos", "Maria"]
    })

    with pytest.raises(ValueError, match="IDs duplicados"):
        transformar_clientes(clientes)


# TESTES DE PRODUTOS

def test_transformar_produtos():
    produtos = pd.DataFrame({
        "produto_id": [101, 102],
        "preco_unitario": [100.00, 200.00],
        "custo_unitario": [60.00, 120.00]
    })

    resultado = transformar_produtos(produtos)

    assert len(resultado) == 2
    assert (resultado["preco_unitario"] > 0).all()


def test_produtos_com_valores_ausentes():
    produtos = pd.DataFrame({
        "produto_id": [101, 102],
        "preco_unitario": [100.00, None],
        "custo_unitario": [60.00, 50.00]
    })

    with pytest.raises(ValueError, match="valores ausentes"):
        transformar_produtos(produtos)


def test_produtos_com_precos_invalidos():
    produtos = pd.DataFrame({
        "produto_id": [101, 102],
        "preco_unitario": [100.00, 0.00],
        "custo_unitario": [60.00, 50.00]
    })

    with pytest.raises(ValueError, match="preços inválidos"):
        transformar_produtos(produtos)


def test_produtos_com_custos_invalidos():
    produtos = pd.DataFrame({
        "produto_id": [101, 102],
        "preco_unitario": [100.00, 200.00],
        "custo_unitario": [60.00, -10.00]
    })

    with pytest.raises(ValueError, match="custos inválidos"):
        transformar_produtos(produtos)


# TESTES DE VENDAS

def test_transformar_vendas():
    vendas = pd.DataFrame({
        "venda_id": [1001, 1002],
        "quantidade": [2, 3],
        "valor_unitario": [100.00, 50.00]
    })

    resultado = transformar_vendas(vendas)

    assert len(resultado) == 2
    assert (resultado["quantidade"] > 0).all()


def test_vendas_com_valores_ausentes():
    vendas = pd.DataFrame({
        "venda_id": [1001, 1002],
        "quantidade": [2, 3],
        "valor_unitario": [100.00, None]
    })

    with pytest.raises(ValueError, match="valores ausentes"):
        transformar_vendas(vendas)


def test_vendas_com_ids_duplicados():
    vendas = pd.DataFrame({
        "venda_id": [1001, 1001],
        "quantidade": [2, 3],
        "valor_unitario": [100.00, 50.00]
    })

    with pytest.raises(ValueError, match="IDs duplicados"):
        transformar_vendas(vendas)


def test_vendas_com_quantidades_invalidas():
    vendas = pd.DataFrame({
        "venda_id": [1001, 1002],
        "quantidade": [2, 0],
        "valor_unitario": [100.00, 50.00]
    })

    with pytest.raises(ValueError, match="quantidades inválidas"):
        transformar_vendas(vendas)


def test_vendas_com_valores_unitarios_invalidos():
    vendas = pd.DataFrame({
        "venda_id": [1001, 1002],
        "quantidade": [2, 3],
        "valor_unitario": [100.00, -50.00]
    })

    with pytest.raises(ValueError, match="valores unitários inválidos"):
        transformar_vendas(vendas)

# TESTES DE RELACIONAMENTOS

def test_validar_relacionamentos_com_clientes_invalidos():
    clientes = pd.DataFrame({"cliente_id": [1, 2]})
    produtos = pd.DataFrame({"produto_id": [101, 102]})

    vendas = pd.DataFrame({
        "venda_id": [1001, 1002],
        "cliente_id": [1, 99],
        "produto_id": [101, 102]
    })

    with pytest.raises(ValueError, match="clientes inexistentes"):
        validar_relacionamentos(clientes, produtos, vendas)


def test_validar_relacionamentos_com_produtos_invalidos():
    clientes = pd.DataFrame({"cliente_id": [1, 2]})
    produtos = pd.DataFrame({"produto_id": [101, 102]})

    vendas = pd.DataFrame({
        "venda_id": [1001, 1002],
        "cliente_id": [1, 2],
        "produto_id": [101, 999]
    })

    with pytest.raises(ValueError, match="produtos inexistentes"):
        validar_relacionamentos(clientes, produtos, vendas)


# TESTES DE DATAS

def test_transformar_datas():
    clientes = pd.DataFrame({
        "data_cadastro": ["2025-01-10", "2025-02-15"]
    })

    vendas = pd.DataFrame({
        "data_venda": ["2025-06-01", "2025-06-02"]
    })

    clientes, vendas = transformar_datas(clientes, vendas)

    assert pd.api.types.is_datetime64_any_dtype(
        clientes["data_cadastro"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        vendas["data_venda"]
    )


# TESTES DE CÁLCULO

def test_calcular_total_vendas():
    vendas = pd.DataFrame({
        "quantidade": [2, 3],
        "valor_unitario": [100.00, 50.00]
    })

    resultado = calcular_total_vendas(vendas)

    assert resultado["valor_total"].tolist() == [200.00, 150.00]
    assert resultado["valor_total"].sum() == 350.00
