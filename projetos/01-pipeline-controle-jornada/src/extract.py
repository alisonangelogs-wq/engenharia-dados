from pathlib import Path

import pandas as pd


COLUNAS_OBRIGATORIAS = [
    "employee_id",
    "work_date",
    "check_in",
    "lunch_out",
    "lunch_in",
    "check_out",
]


def extract_data(caminho=None):
    """Lê o CSV e verifica a presença das colunas obrigatórias."""

    if caminho is None:
        caminho = Path(__file__).resolve().parents[1] / "dados" / "funcionarios.csv"
    else:
        caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho, dtype={"employee_id": "string"})

    colunas_ausentes = [
        coluna for coluna in COLUNAS_OBRIGATORIAS
        if coluna not in df.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {colunas_ausentes}"
        )

    # A primeira linha de dados do CSV corresponde à linha 2 do arquivo.
    df["source_row"] = range(2, len(df) + 2)

    return df
